from pymongo import MongoClient
from bson.objectid import ObjectId

class AnimalShelter(object):
    """CRUD operations for Animal collection in MongoDB"""

    def __init__(self, username, password):
        """Initialize connection to MongoDB"""
        DB = 'AAC'
        COL = 'animals'
        self.client = MongoClient("mongodb://localhost:27017")
        self.database = self.client[DB]
        self.collection = self.database[COL]

    def create(self, data):
        """Insert a new document into the animals collection"""
        if data is not None and isinstance(data, dict):
            try:
                self.collection.insert_one(data)
                return True
            except Exception as e:
                print(f"Error inserting data: {e}")
                return False
        else:
            raise Exception("Invalid data. Must be a non-empty dictionary.")

    def read(self, query):
        """Read documents from the animals collection"""
        try:
            cursor = self.collection.find(query)
            return list(cursor)
        except Exception as e:
            print(f"Error reading data: {e}")
            return []

    def update(self, query, new_values):
        """Update documents in the collection that match the query"""
        if query and new_values:
            try:
                result = self.collection.update_many(query, {'$set': new_values})
                return result.modified_count
            except Exception as e:
                print(f"Error updating data: {e}")
                return 0
        else:
            raise Exception("Both query and new_values must be provided.")

    def delete(self, query):
        """Delete documents in the collection that match the query"""
        if query:
            try:
                result = self.collection.delete_many(query)
                return result.deleted_count
            except Exception as e:
                print(f"Error deleting data: {e}")
                return 0
        else:
            raise Exception("Query must be provided for deletion.")