from flask import Flask, jsonify, request
from db import collection


app = Flask(__name__)


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
