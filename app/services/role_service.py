from app.models.role import Role, db
from flask import request


def create_role():
    data = request.get_json()  # Expecting a list of roles
    if not isinstance(data, list):
        return {
            "status_code": 400,
            "message": "Invalid input format. Expected a list of roles."
        }

    try:
        roles = []
        for item in data:
            if 'role_type' not in item:
                return {
                    "status_code": 400,
                    "message": "Missing 'role_type' in input data."
                }
            new_role = Role(role_type=item['role_type'])
            db.session.add(new_role)
            db.session.commit()
            roles.append({
                "id": new_role.id,
                "role_type": new_role.role_type
            })

        return {
            "status_code": 200,
            "message": "Roles Added Successfully",
            "roles": roles
        }
    except Exception as e:
        db.session.rollback()
        return {
            "status_code": 500,
            "message": f"SQL Exception: {str(e)}"
        }
    finally:
        db.session.remove()

def get_roles():
    roles = Role.query.all()
    return [{"id": role.id, "role_type": role.role_type} for role in roles]

def get_role_by_id(role_id):
    role = Role.query.filter_by(id=role_id).first()
    if role:
        return {"id": role.id, "role_type": role.role_type}
    else:
        return None
