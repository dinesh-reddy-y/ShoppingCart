from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config


db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize SQLAlchemy and Migrate
    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints
    from app.routes.user_routes import user_bp
    from app.routes.role_routes import role_bp
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(role_bp, url_prefix='/api/roles')

    with app.app_context():
        from app.models import user, role, user_role_map

    return app