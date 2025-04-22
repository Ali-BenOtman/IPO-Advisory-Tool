from flask import jsonify
from werkzeug.exceptions import HTTPException
from bson.errors import InvalidId
from typing import Tuple, Dict, Any

class APIError(Exception):
    def __init__(self, message: str, status_code: int = 400, payload: Dict = None):
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def to_dict(self) -> Dict[str, Any]:
        rv = dict(self.payload or ())
        rv['message'] = self.message
        rv['status'] = 'error'
        return rv

def handle_api_error(error: APIError) -> Tuple[Dict, int]:
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

def handle_http_error(error: HTTPException) -> Tuple[Dict, int]:
    response = jsonify({
        'status': 'error',
        'message': error.description,
        'code': error.code
    })
    response.status_code = error.code
    return response

def handle_invalid_id(error: InvalidId) -> Tuple[Dict, int]:
    response = jsonify({
        'status': 'error',
        'message': 'Invalid ID format',
        'code': 400
    })
    response.status_code = 400
    return response

def handle_generic_error(error: Exception) -> Tuple[Dict, int]:
    response = jsonify({
        'status': 'error',
        'message': 'An unexpected error occurred',
        'code': 500
    })
    response.status_code = 500
    return response 