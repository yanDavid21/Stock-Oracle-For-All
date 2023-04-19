from pymongo import MongoClient


# Replace the connection string with your own if needed
client = MongoClient("mongodb://localhost:27017/")
db = client['stock_oracle_db']
stock_collection = db['stocks']
