# Client-Server-Development
CS 340 Client/Server Development

# **Grazioso Salvare Dog Rescue Dashboard – CS 340 Portfolio Artifact**

**Project Overview**

This project showcases a data dashboard built for Grazioso Salvare, a dog rescue organization, to help them quickly identify adoptable dogs suited for specialized rescue roles such as mountain, wilderness, and water rescues. It includes an interactive Jupyter Notebook dashboard, database queries using MongoDB, and a Python-based CRUD module to interact with the data.

**Reflection**

Writing maintainable, readable, and adaptable programs:
One of the key elements of this project was writing the crud.py Python module, which served as the bridge between the MongoDB database and the dashboard interface. To ensure maintainability and readability, I followed consistent naming conventions, added meaningful comments, and organized functions with clear purposes (e.g., create, read, update, delete). Structuring the module this way made it easy to reuse when developing the Project Two dashboard in the Jupyter Notebook. This modular approach allowed me to separate concerns — keeping database logic distinct from visualization — which is not only good design practice but also makes future updates more manageable. I could easily adapt this CRUD module to connect other front-end tools or support different types of queries in future projects.

**Approaching problems as a computer scientist:**

When building the dashboard and querying the animal shelter database, I first analyzed the client's needs and constraints. Grazioso Salvare had specific criteria for rescue dogs (age range, breed, sex, etc.), which I translated into well-structured MongoDB queries. Compared to earlier courses, I noticed I was more methodical and confident in breaking down client requirements, validating them against the data structure, and using filtering techniques efficiently. In future database projects, I would continue using a step-by-step process: understand the client's end goal, structure the data appropriately, and build reusable components for interaction.

**What computer scientists do and why it matters:**

Computer scientists solve real-world problems using data, logic, and technology. In this project, I enabled a dog rescue organization to operate more efficiently by helping them visualize and access key data insights. A well-designed dashboard like this supports better decision-making, reduces time spent filtering through data manually, and improves the speed and accuracy of finding the right rescue animals. These types of solutions have a real impact on how organizations function, ultimately saving time, resources, and — in the case of Grazioso Salvare — potentially saving lives.

**Repository Contents**

ProjectTwoDashboard.ipynb: Interactive Jupyter Notebook dashboard

crud.py: Python module for database interactions

7_Readme.docx: Word document detailing implementation steps, tools used, and screenshots

**Portfolio Relevance**

This artifact highlights my ability to integrate backend database functionality with a usable front-end interface, reinforcing core computer science principles like modularity, abstraction, and client-focused development. It's a strong example of full-cycle project development and a useful demonstration for future employers.
