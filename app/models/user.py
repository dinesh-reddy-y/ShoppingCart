import uuid
from app import db
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from app.models.audit_columns import Audit_Columns

class User(db.Model, Audit_Columns):
    __tablename__ = 'users'

    id = db.Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mobile_number = db.Column(db.String(10), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    roles = db.relationship(
        'Role',
        secondary='user_role_map',
        primaryjoin='User.id == user_role_map.c.user_id',
        secondaryjoin='Role.id == user_role_map.c.role_id',
        back_populates='users',
        lazy='joined'
    )

    def __repr__(self):
        return f'<User {self.username}>'

    def to_dict(self):
        return{
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "mobile_number": self.mobile_number,
            "password": self.password
        }
