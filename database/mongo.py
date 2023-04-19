from pymongo import MongoClient


class MongoAPI:
    def __init__(self):
        # Replace the connection string with your own if needed
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["myDatabase"]
        self.collection = self.db["myCollection"]

    def insert_into_collection(self, record):
        self.collection.insert_one(record)
