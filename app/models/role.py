import uuid
from app import db
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from app.models.audit_columns import Audit_Columns

class Role(db.Model, Audit_Columns):
    __tablename__ = 'roles'

    id = db.Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    role_type = db.Column(db.String(80), unique=True, nullable=False)

    users = db.relationship(
        'User',
        secondary='user_role_map',
        primaryjoin='Role.id == user_role_map.c.role_id',
        secondaryjoin='User.id == user_role_map.c.user_id',
        back_populates='roles',
        lazy='joined'
    )

    def __repr__(self):
        return f'<Role {self.role_type}>'

    def to_dict(self):
        return {
            'id': self.id,
            'role_type': self.role_type
        }
