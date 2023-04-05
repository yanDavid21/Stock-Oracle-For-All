from pymongo import MongoClient


# Replace the connection string with your own if needed
client = MongoClient("mongodb://localhost:27017/")
db = client["myDatabase"]
collection = db["myCollection"]
