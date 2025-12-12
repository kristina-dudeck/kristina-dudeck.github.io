from pymongo import MongoClient, errors
import os

class AnimalShelter(object):
    """Enhanced CRUD operations for Animal collection in MongoDB"""

    def __init__(self, username=None, password=None, host="localhost", port=27017):
        """
        Initialize connection to MongoDB with optional credential handling
        and automatic index creation for performance.
        """
        DB = 'AAC'
        COL = 'animals'

        # Use environment variables if username/password not provided
        username = username or os.getenv("MONGO_USER")
        password = password or os.getenv("MONGO_PASS")

        try:
            if username and password:
                # Authenticated connection
                self.client = MongoClient(
                    f"mongodb://{host}:{port}",
                    username=username,
                    password=password,
                    serverSelectionTimeoutMS=5000
                )
            else:
                # Local connection without authentication
                self.client = MongoClient(f"mongodb://{host}:{port}", serverSelectionTimeoutMS=5000)

            self.database = self.client[DB]
            self.collection = self.database[COL]

            # Create indexes on common query fields for faster lookups
            self.collection.create_index("animal_type")
            self.collection.create_index("breed")
            self.collection.create_index("location")
            self.collection.create_index("age_upon_outcome")

        except errors.ConnectionFailure as e:
            raise Exception(f"Database connection failed: {e}")

    def sanitize_query(self, query):
        """Validate and sanitize query to allow only expected keys."""
        allowed_keys = {"animal_type", "breed", "location", "age_upon_outcome", "_id"}
        return {k: v for k, v in (query or {}).items() if k in allowed_keys}

    def create(self, data):
        """Insert a new document into the animals collection"""
        if data and isinstance(data, dict):
            try:
                result = self.collection.insert_one(data)
                return str(result.inserted_id)
            except Exception as e:
                print(f"Error inserting data: {e}")
                return None
        else:
            raise ValueError("Invalid data. Must be a non-empty dictionary.")

    def read(self, query=None, projection=None, limit=0):
        """Read documents from the animals collection"""
        try:
            query = self.sanitize_query(query or {})
            cursor = self.collection.find(query, projection or {"_id": 0}).limit(limit)
            return list(cursor)
        except Exception as e:
            print(f"Error reading data: {e}")
            return []

    def update(self, query, new_values):
        """Update documents in the collection that match the query"""
        if query and new_values:
            try:
                query = self.sanitize_query(query)
                result = self.collection.update_many(query, {'$set': new_values})
                return result.modified_count
            except Exception as e:
                print(f"Error updating data: {e}")
                return 0
        else:
            raise ValueError("Both query and new_values must be provided.")

    def delete(self, query):
        """Delete documents in the collection that match the query"""
        if query:
            try:
                query = self.sanitize_query(query)
                result = self.collection.delete_many(query)
                return result.deleted_count
            except Exception as e:
                print(f"Error deleting data: {e}")
                return 0
        else:
            raise ValueError("Query must be provided for deletion.")