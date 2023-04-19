from bson import json_util
from flask import Flask, request, jsonify, render_template
from db import stock_collection
import sys
import os
from flask_cors import CORS
import json


sys.path.append(os.getcwd())

app = Flask(__name__, static_folder="./frontend/build/static",
            template_folder="./frontend/build")
CORS(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/items', methods=['GET'])
def get_items():
    items = []
    for item in stock_collection.find():
        item['_id'] = str(item['_id'])
        items.append(item)
    return jsonify(items)


@app.route('/stock', methods=['GET'])
def get_stock():
    ticker = request.args.get('ticker')
    if ticker:
        stock = stock_collection.find({"ticker": ticker.upper()})
        if stock:

            return json_util.dumps(stock), 200
        else:
            return json.dumps([]), 200
    else:
        return jsonify({"error": "Ticker parameter is required"}), 400
