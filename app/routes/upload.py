from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os

from app import create_app

upload_bp = Blueprint('upload', __name__)

# Set the file upload folder path
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Function to check if the file is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_bp.route('/upload_file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"msg": "No file part"}), 400
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))  # Save file locally

        # Store file metadata in MongoDB
        app = create_app()
        files_collection = app.db.files
        file_metadata = {
            'filename': filename,
            'status': 'uploaded'
        }
        files_collection.insert_one(file_metadata)

        return jsonify({"msg": "File uploaded successfully"}), 200
    else:
        return jsonify({"msg": "Invalid file type"}), 400
