from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from app.models import db
from app.jwt_keys import generate_jwt_key
from dotenv import load_dotenv
from pathlib import Path
from datetime import timedelta

def create_app():
    load_dotenv(dotenv_path=Path("instance/secret.env"))
    
    app = Flask(__name__)
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI="sqlite:///database.db",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JWT_SECRET_KEY=generate_jwt_key(32),
        JWT_ACCESS_TOKEN_EXPIRES=timedelta(minutes=15)
    )
    
    # Initialize extensions
    db.init_app(app)
    api = Api(app)
    jwt = JWTManager(app)
    
    # Register blueprints
    from app.auth.routes import auth_bp
    from app.user.routes import user_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app