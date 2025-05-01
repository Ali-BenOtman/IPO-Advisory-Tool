from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from datetime import datetime

client = MongoClient("mongodb://localhost:27017/")
db = client.ipo  

# Collections
users = db.users
users.create_index("username", unique=True) #no duplicates
files = db.files
predictions = db.predictions

# role-based permissions
roles = db.roles
roles.insert_many([
    {"_id": 1, "name": "admin", "permissions": ["read", "write", "delete"]},
    {"_id": 2, "name": "analyst", "permissions": ["read", "write"]},
    {"_id": 3, "name": "viewer", "permissions": ["read"]}
])
print("Database Connected!")