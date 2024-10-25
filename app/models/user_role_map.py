import uuid
from app import db
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from app.models.audit_columns import Audit_Columns

class UserRoleMap(db.Model, Audit_Columns):
    __tablename__ = "user_role_map"

    id = db.Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(PG_UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    role_id = db.Column(PG_UUID(as_uuid=True), db.ForeignKey('roles.id'), nullable=False)

    def __repr__(self):
        return f'<UserRoleMap user_id={self.user_id} role_id={self.role_id}>'
