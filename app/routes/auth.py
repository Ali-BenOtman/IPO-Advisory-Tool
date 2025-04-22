from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_restx import Namespace, Resource, fields
from app import create_app
import bcrypt

auth_bp = Blueprint('auth', __name__)
api = Namespace('auth', description='Authentication operations')

# Define models for request/response documentation
user_model = api.model('User', {
    'email': fields.String(required=True, description='User email address'),
    'password': fields.String(required=True, description='User password'),
    'name': fields.String(description='User full name')
})

login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email address'),
    'password': fields.String(required=True, description='User password')
})

token_model = api.model('Token', {
    'access_token': fields.String(description='JWT access token'),
    'msg': fields.String(description='Response message')
})

@api.route('/register')
class Register(Resource):
    @api.doc('create_user')
    @api.expect(user_model)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Validation Error')
    def post(self):
        """Register a new user"""
        app = create_app()
        user_data = request.get_json()

        # Hash password before saving
        hashed_password = bcrypt.hashpw(user_data['password'].encode('utf-8'), bcrypt.gensalt())

        # Insert user into MongoDB
        users_collection = app.db.users
        user_data['password'] = hashed_password
        new_user = users_collection.insert_one(user_data)

        return {"msg": "User registered successfully", "user_id": str(new_user.inserted_id)}, 201

@api.route('/login')
class Login(Resource):
    @api.doc('login_user')
    @api.expect(login_model)
    @api.response(200, 'Login successful', token_model)
    @api.response(401, 'Invalid credentials')
    def post(self):
        """Login user and return token"""
        app = create_app()
        user_data = request.get_json()

        users_collection = app.db.users
        user = users_collection.find_one({'email': user_data['email']})

        if user and bcrypt.checkpw(user_data['password'].encode('utf-8'), user['password']):
            access_token = create_access_token(identity=str(user['_id']))
            return {"msg": "Login successful", "access_token": access_token}, 200
        else:
            return {"msg": "Invalid credentials"}, 401

@api.route('/protected')
class Protected(Resource):
    @api.doc('get_protected_resource')
    @api.response(200, 'Success')
    @api.response(401, 'Unauthorized')
    @jwt_required()
    def get(self):
        """Get protected resource"""
        current_user = get_jwt_identity()
        return {"logged_in_as": current_user}, 200
