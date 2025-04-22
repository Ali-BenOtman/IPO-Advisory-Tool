from flask import Flask
from pymongo import MongoClient
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.exceptions import HTTPException
from bson.errors import InvalidId
from flask_restx import Api
from flask_talisman import Talisman
from app.config import config
from app.middleware.error_handler import (
    APIError, handle_api_error, handle_http_error,
    handle_invalid_id, handle_generic_error
)
import os

def create_app(config_name='default'):
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    CORS(app, resources={r"/api/*": {"origins": os.getenv('ALLOWED_ORIGINS', '*')}})
    jwt = JWTManager(app)
    
    # Initialize security headers
    csp = {
        'default-src': "'self'",
        'img-src': "'self' data: https:",
        'script-src': "'self' 'unsafe-inline' 'unsafe-eval'",
        'style-src': "'self' 'unsafe-inline'",
        'font-src': "'self' data: https:",
    }
    
    Talisman(
        app,
        force_https=False,  # Set to True in production
        strict_transport_security=True,
        session_cookie_secure=True,
        content_security_policy=csp,
        content_security_policy_nonce_in=['script-src'],
        feature_policy={
            'geolocation': "'self'",
            'camera': "'none'",
            'microphone': "'none'",
            'payment': "'none'",
        }
    )
    
    # Initialize API documentation
    api = Api(
        app,
        version='1.0',
        title='IPO Backend API',
        description='A Flask-based backend API for IPO management',
        doc='/api/docs',
        prefix='/api'
    )
    
    # Initialize rate limiter
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"]
    )
    
    # MongoDB Connection
    client = MongoClient(app.config['MONGODB_URI'])
    app.db = client[app.config['MONGODB_DB']]
    
    # Register error handlers
    app.register_error_handler(APIError, handle_api_error)
    app.register_error_handler(HTTPException, handle_http_error)
    app.register_error_handler(InvalidId, handle_invalid_id)
    app.register_error_handler(Exception, handle_generic_error)
    
    # Import and register API namespaces
    from app.routes.auth import api as auth_ns
    api.add_namespace(auth_ns, path='/auth')
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.user import user_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(user_bp, url_prefix='/api/users')
    
    return app
