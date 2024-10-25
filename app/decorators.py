# decorators.py
from flask import request, jsonify
import jwt
from functools import wraps
import os

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Look for token in Authorization header
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]  # Bearer token

        if not token:
            return jsonify({"message": "Token is missing!"}), 401

        try:
            # Decode the token
            data = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=[os.getenv('ALGORITHM')])
            # Add any additional logic here, such as user validation
        except Exception as e:
            return jsonify({"message": "Token is invalid or expired!"}), 401

        return f(*args, **kwargs)

    return decorated