from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

# Replace the connection string with your own if needed
client = MongoClient("mongodb://localhost:27017/")
db = client["myDatabase"]
collection = db["myCollection"]

@app.route('/')
def index():
    return "Welcome to the Flask MongoDB API"

@app.route('/items', methods=['GET'])
def get_items():
    items = []
    for item in collection.find():
        item['_id'] = str(item['_id'])
        items.append(item)
    return jsonify(items)

@app.route('/item', methods=['POST'])
def add_item():
    data = request.get_json()
    new_item = {
        "name": data['name'],
        "description": data['description'],
    }
    collection.insert_one(new_item)
    return jsonify({"message": "Item added successfully"})

if __name__ == '__main__':
    app.run(debug=True)
