from flask import Blueprint, request, jsonify
from app.services.role_service import create_role, get_roles, get_role_by_id

# Create a Blueprint instance
role_bp = Blueprint('roles', __name__)

@role_bp.route('/get-all-roles', methods=['GET'])
def list_roles():
    roles = get_roles()
    return jsonify(roles)

@role_bp.route('/add-role', methods=['POST'])
def add_role():
    response = create_role()
    if response['status_code'] == 200:
        return jsonify(response), 201
    else:
        return jsonify(response), 500

@role_bp.route('/get-role/<uuid:role_id>', methods=['GET'])
def get_role(role_id):
    role = get_role_by_id(role_id)
    if role:
        return jsonify(role)
    else:
        return jsonify({"error": "Role not found"}), 404