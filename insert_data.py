from database import users, files, predictions
from bson import ObjectId
from datetime import datetime
from werkzeug.security import generate_password_hash
import sys

print("🚀 Launching data insertion...")

try:
    # Insert Admin
    admin = {
        "_id": ObjectId(),
        "username": "admin",
        "password": generate_password_hash("admin123"),
        "created_at": datetime.utcnow()
    }
    users.insert_one(admin)
    
    # Insert File
    file = {
        "file_id": ObjectId(),
        "user_id": admin["_id"],
        "filename": "test.xlsx"
    }
    files.insert_one(file)
    
    print("✅ Success! Inserted:")
    print(f"- Admin ID: {admin['_id']}")
    print(f"- File ID: {file['file_id']}")
    
except Exception as e:
    print(f"❌ CRASHED: {type(e).__name__}", file=sys.stderr)
    print(f"Error details: {e}", file=sys.stderr)