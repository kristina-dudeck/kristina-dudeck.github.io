# %%
from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output
import dash_leaflet as dl
import plotly.express as px
import base64
import pandas as pd
import os

from crud import AnimalShelter

# Connect to MongoDB
username = "aacuser"
password = "SNHU1234"
db = AnimalShelter(username, password)

# Load logo
image_filename = 'grazioso_logo.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

# %%
# Initialize Dash app
app = Dash(__name__)

# Layout
app.layout = html.Div([
    html.Center(html.B(html.H1('CS-340 Dashboard'))),
    html.Center(html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()), style={'height': '100px'})),
    html.Center(html.P("Kristina Dudeck • Grazioso Salvare • Fall 2025")),
    html.Hr(),

    html.Div([
        html.Label("Filter by Rescue Type:"),
        dcc.RadioItems(
            id='filter-type',
            options=[
                {'label': 'Water', 'value': 'water'},
                {'label': 'Mountain', 'value': 'mountain'},
                {'label': 'Disaster', 'value': 'disaster'},
                {'label': 'All', 'value': 'all'}
            ],
            value='all',
            labelStyle={'display': 'inline-block', 'margin-right': '10px'}
        )
    ], style={'padding': '10px'}),

    html.Hr(),

    dash_table.DataTable(
        id='datatable-id',
        columns=[],
        data=[],
        page_size=10,
        page_current=0,
        sort_action='native',
        sort_mode='multi',
        row_selectable='single',
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left'},
        style_header={'backgroundColor': 'lightgrey', 'fontWeight': 'bold'},
        style_data_conditional=[]
    ),

    html.Br(),
    html.Hr(),

    html.Div([
        html.Div(id='graph-id', style={'width': '48%', 'height': '450px', 'display': 'inline-block'}),
        html.Div(id='map-id', style={'width': '48%', 'height': '450px', 'display': 'inline-block', 'marginLeft': '4%'})
    ], style={'display': 'flex', 'justifyContent': 'space-between'}),

], style={'padding': '20px'})

# %%
@app.callback(
    [Output('datatable-id', 'data'),
     Output('datatable-id', 'columns')],
    [Input('filter-type', 'value')]
)
def update_dashboard(filter_type):
    """Update data table based on selected rescue type"""
    try:
        if filter_type == 'water':
            query = {"animal_type": "Dog", "breed": {"$in": ["Labrador Retriever Mix"]}}
        elif filter_type == 'mountain':
            query = {"animal_type": "Dog", "breed": {"$in": ["German Shepherd"]}}
        elif filter_type == 'disaster':
            query = {"animal_type": "Dog", "breed": {"$in": ["Doberman Pinscher", "Golden Retriever"]}}
        else:
            query = {}

        results = db.read(query)
        if results:
            df_filtered = pd.DataFrame.from_records(results)
            if '_id' in df_filtered.columns:
                df_filtered.drop(columns=['_id'], inplace=True)
            columns = [{"name": i, "id": i, "deletable": False, "selectable": True} for i in df_filtered.columns]
            return df_filtered.to_dict('records'), columns
        else:
            return [], []
    except Exception as e:
        print(f"Error updating dashboard: {e}")
        return [], []

@app.callback(
    Output('graph-id', "children"),
    [Input('datatable-id', "derived_virtual_data")]
)
def update_graphs(viewData):
    """Generate pie chart of breed distribution"""
    if not viewData:
        return [html.P("No data available for chart.")]
    try:
        dff = pd.DataFrame.from_dict(viewData)
        fig = px.pie(dff, names='breed', title='Breed Distribution')
        fig.update_layout(
            height=480,
            margin=dict(t=30, b=60, l=30, r=30),
            legend=dict(
                font=dict(size=9),
                orientation="h",
                x=0.5,
                y=-0.25,
                xanchor="center",
                yanchor="top",
                itemwidth=90,
                bgcolor="rgba(255,255,255,0.5)",
                bordercolor="gray",
                borderwidth=1
            )
        )
        return [dcc.Graph(figure=fig, style={'height': '480px', 'width': '100%', 'padding': '0px'})]
    except Exception as e:
        print(f"Error generating chart: {e}")
        return [html.P("Error generating chart.")]

@app.callback(
    Output('datatable-id', 'style_data_conditional'),
    [Input('datatable-id', 'selected_columns')]
)
def update_styles(selected_columns):
    """Highlight selected columns in data table"""
    if selected_columns is None:
        return []
    return [{
        'if': {'column_id': i},
        'background_color': '#D2F3FF'
    } for i in selected_columns]

@app.callback(
    Output('map-id', "children"),
    [Input('datatable-id', "derived_virtual_data"),
     Input('datatable-id', "derived_virtual_selected_rows")]
)
def update_map(viewData, index):
    """Display map with selected animal's location"""
    if not viewData:
        return [html.P("No data available to display on map.")]
    try:
        dff = pd.DataFrame.from_dict(viewData)
        row = index[0] if index else 0
        lat = float(dff.loc[row, 'location_lat'])
        lon = float(dff.loc[row, 'location_long'])
        return [
            dl.Map(style={'width': '1000px', 'height': '500px'}, center=[lat, lon], zoom=10, children=[
                dl.TileLayer(id="base-layer-id"),
                dl.Marker(position=[lat, lon], children=[
                    dl.Tooltip(dff.loc[row, 'breed']),
                    dl.Popup([
                        html.H1("Animal Name"),
                        html.P(dff.loc[row, 'name'])
                    ])
                ])
            ])
        ]
    except (KeyError, ValueError, IndexError) as e:
        print(f"Error displaying map: {e}")
        return [html.P("Selected record is missing location data.")]

# %%
# Run the app
if __name__ == '__main__':
    app.run(debug=True)

# %%
# Optional: Insert sample data for testing
sample_animals = [
    {"animal_type": "Dog", "breed": "Labrador Retriever Mix", "name": "Buddy", "location_lat": 30.75, "location_long": -97.48},
    {"animal_type": "Dog", "breed": "German Shepherd", "name": "Rex", "location_lat": 30.76, "location_long": -97.49},
    {"animal_type": "Dog", "breed": "Golden Retriever", "name": "Sunny", "location_lat": 30.77, "location_long": -97.50},
    {"animal_type": "Dog", "breed": "Doberman Pinscher", "name": "Max", "location_lat": 30.78, "location_long": -97.51}
]

for animal in sample_animals:
    db.create(animal)

print("Sample data inserted.")


