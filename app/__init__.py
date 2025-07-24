from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from app.models import db
from app.jwt_keys import generate_jwt_key #local module buat generate JWT secret key
from datetime import timedelta


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI="sqlite:///database.db",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JWT_SECRET_KEY=generate_jwt_key(32),
        JWT_ACCESS_TOKEN_EXPIRES=timedelta(minutes=30)
    )
    
    # initialize extensions
    db.init_app(app)
    api = Api(app)
    jwt = JWTManager(app)
    
    #register blueprints
    from app.auth.routes import auth_bp
    from app.user.routes import user_bp
    from app.services.routes import services_bp
    
    app.register_blueprint(auth_bp, url_prefix = "/auth")
    app.register_blueprint(user_bp, url_prefix = "/user")
    app.register_blueprint(services_bp, url_prefix ="/services")
    
    #buat database tables
    with app.app_context():
        db.create_all()
    
    return app
