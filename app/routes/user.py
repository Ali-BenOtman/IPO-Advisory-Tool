from flask import Blueprint, request, jsonify
from app import create_app

user_bp = Blueprint('user', __name__)

# Create a new user
@user_bp.route('/add_user', methods=['POST'])
def add_user():
    app = create_app()
    user_data = request.get_json()  # Get JSON data from the request
    users_collection = app.db.users  # Access the 'users' collection in MongoDB

    # Insert the new user into the MongoDB collection
    new_user = users_collection.insert_one(user_data)
    
    # Return success response with user ID
    return jsonify({"msg": "User added successfully", "user_id": str(new_user.inserted_id)}), 201
# Get all users
@user_bp.route('/get_users', methods=['GET'])
def get_users():
    app = create_app()
    users_collection = app.db.users  # Access the 'users' collection in MongoDB

    # Retrieve all users from the collection
    users = users_collection.find()
    users_list = list(users)  # Convert cursor to list for JSON compatibility
    
    return jsonify({"users": users_list}), 200
# Update a user's details
@user_bp.route('/update_user/<user_id>', methods=['PUT'])
def update_user(user_id):
    app = create_app()
    user_data = request.get_json()  # Get JSON data from the request
    users_collection = app.db.users  # Access the 'users' collection

    # Update the user with the specified user_id
    result = users_collection.update_one({'_id': user_id}, {"$set": user_data})
    
    if result.matched_count > 0:
        return jsonify({"msg": "User updated successfully"}), 200
    else:
        return jsonify({"msg": "User not found"}), 404
# Delete a user
@user_bp.route('/delete_user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    app = create_app()
    users_collection = app.db.users  # Access the 'users' collection

    # Delete the user with the specified user_id
    result = users_collection.delete_one({'_id': user_id})

    if result.deleted_count > 0:
        return jsonify({"msg": "User deleted successfully"}), 200
    else:
        return jsonify({"msg": "User not found"}), 404
