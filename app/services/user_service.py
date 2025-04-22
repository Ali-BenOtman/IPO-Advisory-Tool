from app import create_app
import bcrypt
from bson import ObjectId
from typing import Dict, List, Optional

class UserService:
    def __init__(self):
        app = create_app()
        self.users_collection = app.db.users

    def create_user(self, user_data: Dict) -> Dict:
        """Create a new user with hashed password."""
        if 'password' in user_data:
            user_data['password'] = bcrypt.hashpw(
                user_data['password'].encode('utf-8'),
                bcrypt.gensalt()
            )
        result = self.users_collection.insert_one(user_data)
        return {"user_id": str(result.inserted_id)}

    def get_user_by_id(self, user_id: str) -> Optional[Dict]:
        """Get user by ID."""
        try:
            return self.users_collection.find_one({'_id': ObjectId(user_id)})
        except:
            return None

    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Get user by email."""
        return self.users_collection.find_one({'email': email})

    def update_user(self, user_id: str, user_data: Dict) -> bool:
        """Update user details."""
        try:
            result = self.users_collection.update_one(
                {'_id': ObjectId(user_id)},
                {"$set": user_data}
            )
            return result.matched_count > 0
        except:
            return False

    def delete_user(self, user_id: str) -> bool:
        """Delete user."""
        try:
            result = self.users_collection.delete_one({'_id': ObjectId(user_id)})
            return result.deleted_count > 0
        except:
            return False

    def get_all_users(self, page: int = 1, per_page: int = 10) -> Dict:
        """Get paginated list of users."""
        skip = (page - 1) * per_page
        total = self.users_collection.count_documents({})
        users = list(self.users_collection.find().skip(skip).limit(per_page))
        return {
            "users": users,
            "total": total,
            "page": page,
            "per_page": per_page,
            "total_pages": (total + per_page - 1) // per_page
        } 