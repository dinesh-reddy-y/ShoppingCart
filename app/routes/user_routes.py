from flask import Blueprint, request, jsonify
from app.decorators import token_required
from app.services.user_service import create_user, get_users, user_login

# Create a Blueprint instance
user_bp = Blueprint('users', __name__)


@user_bp.route('/add-user', methods=['POST'])
def add_user():
    user = create_user()
    return user, 200


@user_bp.route('/get-all-users', methods=['GET'])
@token_required
def list_users():
    users = get_users()
    return jsonify(users)

@user_bp.route('/login', methods=['POST'])
def login():
    user = user_login()
    return user