from app import db
from app.models.user import  User
from app.models.user_role_map import UserRoleMap
from app.services.role_service import get_role_by_id
from app.models.role import Role
from flask import jsonify, request
import jwt
import time
import os
import dotenv
from datetime import timedelta, datetime, timezone
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash


def create_user():

    data = request.get_json()
    try:

        hashed_password = generate_password_hash(data['password'])
        # Extract user data
        new_user = User(
            username=data['username'],
            email=data['email'],
            password=hashed_password,
            mobile_number=data['mobile_number']
        )

        # Retrieve role by role_id from the database
        role_data = data['role_type']
        if role_data:
            role = Role.query.filter_by(role_type=role_data).first()
            if role:
                role_id = role.id
                role_type = role.role_type
            else:
                return jsonify({
                    "status_code": 404,
                    "message": f"Role {role_data} not found."
                })

        # Add user to the session
        db.session.add(new_user)
        db.session.commit()

        # Getting new user_id
        new_user_id = new_user.id

        # Creating a new UserRoleMap
        user_role_map = UserRoleMap(
                                    user_id = new_user_id,
                                    role_id= role_id
                                    )

        # Add UserRoleMap to the session
        db.session.add(user_role_map)
        db.session.commit()

        return jsonify({
            "status_code": 200,
            "message": "User added successfully",
            "user": data
        })

    except Exception as e:
        db.session.rollback()  # Rollback transaction in case of failure
        db.session.close()  # Close the session properly
        return jsonify({
            "status_code": 500,
            "message": f"SQL Exception: {str(e)}"
        })


def get_users():
    users = User.query.filter_by(is_deleted=False).all()
    return [user.to_dict() for user in users]


def user_login():
    secret = os.getenv('SECRET_KEY')
    algorithm = os.getenv('ALGORITHM')
    data = request.get_json()

    email = data.get('email')

    if not email:
        return jsonify({
            "status_code": 400,
            "message": "Email is required"
        }), 400  # Return 400 if email is missing

    try:
        # Fetch user from the database using email
        user = User.query.filter_by(email=email).first()

        if user:
            # JWT header and payload
            header = {
                "alg": "HS256",
                "typ": "JWT"
            }
            payload = {
                'user_id': str(user.id),
                'exp': datetime.now(timezone.utc) + timedelta(hours=1)
            }

            # Check if the password matches
            if check_password_hash(user.password, data.get('password')):
                encoded_jwt = jwt.encode(payload, secret, algorithm=algorithm, headers=header)
                return jsonify({
                    "user_id": str(user.id),
                    "email": user.email,
                    "token": encoded_jwt
                }), 200
            else:
                return jsonify({
                    "status_code": 401,
                    "message": "Incorrect password"
                }), 401  # Unauthorized if password doesn't match
        else:
            return jsonify({
                "status_code": 404,
                "message": "User not found"
            }), 404  # User not found
    except SQLAlchemyError as db_error:
        # Catch database errors
        return jsonify({
            "status_code": 500,
            "message": "Database error occurred"
        }), 500  # Return 500 if a database error occurs
    except Exception as e:
        # Catch other exceptions
        return jsonify({
            "status_code": 500,
            "message": "An error occurred: " + str(e)
        }), 500  # General server error
