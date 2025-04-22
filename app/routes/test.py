from flask import Blueprint, jsonify
from app import create_app  # Keep the import here but make sure circular import doesn't happen

test_bp = Blueprint('test', __name__)

# Define your test route here
@test_bp.route('/test_db', methods=['GET'])
def test_db():
    app = create_app()  # Create an app instance here
    try:
        users_collection = app.db.users
        users = users_collection.find()
        return jsonify({"msg": "MongoDB Connection Successful!", "users": list(users)}), 200
    except Exception as e:
        return jsonify({"msg": "Error connecting to MongoDB", "error": str(e)}), 500
