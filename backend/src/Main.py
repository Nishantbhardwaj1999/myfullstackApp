from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
from logger import BaseLogger

app = Flask(__name__)
logger = BaseLogger("flask_app")

client = MongoClient('mongodb://localhost:27017/')
db = client['myfullstackdatabase']
collection = db['owner_name']

@app.route('/items', methods=['POST'])
def create_item():
    logger.info("Received a POST request to create an item")
    data = request.json
    try:
        inserted_item = collection.insert_one(data)
        logger.debug("Item inserted successfully")
        return jsonify(str(inserted_item.inserted_id)), 201
    except Exception as e:
        logger.error(f"Failed to insert item: {e}")
        return jsonify({"message": "Failed to insert item"}), 500

# Read
@app.route('/items/<string:item_id>', methods=['GET'])
def get_item(item_id):
    logger.info("Received a GET request to retrieve an item")
    item = collection.find_one({"_id": ObjectId(item_id)})
    if item:
        item['_id'] = str(item['_id'])  # Convert ObjectId to string
        logger.debug("Item found")
        return jsonify(item), 200
    else:
        logger.warning("Item not found")
        return jsonify({"message": "Item not found"}), 404

@app.route('/items/<string:item_id>', methods=['PUT'])
def update_item(item_id):
    logger.info("Received a PUT request to update an item")
    data = request.json
    if not data:  
        logger.warning("No data provided for update")
        return jsonify({"message": "No data provided for update"}), 400

    # Remove any empty fields from the data
    data = {key: value for key, value in data.items() if value is not None and value != ""}
    
    # Rename keys with dots to use the $set operator properly
    data = {key.replace(".", "_"): value for key, value in data.items()}
    
    updated_item = collection.update_one({"_id": ObjectId(item_id)}, {"$set": data})
    if updated_item.modified_count:
        logger.debug("Item updated successfully")
        return jsonify({"message": "Item updated successfully"}), 200
    else:
        logger.warning("Item not found")
        return jsonify({"message": "Item not found"}), 404

# Delete a single key-value pair from a document
@app.route('/items/<string:item_id>/<string:key>', methods=['DELETE'])
def delete_item_key(item_id, key):
    logger.info(f"Received a DELETE request to delete key '{key}' from item '{item_id}'")
    deleted_item = collection.update_one(
        {"_id": ObjectId(item_id)},
        {"$unset": {key: ""}}  # Use $unset to remove the specified key
    )
    if deleted_item.modified_count:
        logger.debug(f"Key '{key}' deleted successfully")
        return jsonify({"message": f"Key '{key}' deleted successfully"}), 200
    else:
        logger.warning("Item not found or key not present")
        return jsonify({"message": "Item not found or key not present"}), 404

if __name__ == "__main__":
    app.run(debug=True)
