from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required
from app.models import db, User
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user_id = data.get("id", "").strip()
    user_pass = data.get("password", "").strip()
    
    if not user_id or not user_pass:
        abort(400, description="ID or PASS cannot be empty")
        
    listed_user = User.query.get(user_id)
    
    if listed_user and check_password_hash(listed_user.password,user_pass):
        access_token = create_access_token(identity=user_id)
        refresh_token = create_refresh_token(identity=user_id)
        return jsonify({
            "Successful login": f"Welcome back {user_id}",
            "access token": access_token,
            "refresh token": refresh_token
        }), 200
    
    if listed_user:
        return jsonify({"error": "Wrong password"}), 401
    
    return jsonify({"error": "user not in database, please sign up"}), 404

@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    user_id = data.get("id","").strip()
    user_pass = data.get("password", "").strip()
    if len(user_pass) <= 6:
        return jsonify({"error" : "password must be at least 6 charactes, without whitespace(space)"}), 400
    
    if not user_id or not user_pass:
        return jsonify({"error": "ID and password required"}), 400
    
    hashed_pass = generate_password_hash(user_pass)
    listed_user = User.query.get(user_id)
    if listed_user:
        return jsonify({"error": "You already have an account. Try to log in."}), 409
    
    new_user = User(id=user_id, password=hashed_pass)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"Successful sign up": "Your account is now active"}), 201

@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    from flask_jwt_extended import get_jwt_identity, create_access_token
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    return jsonify(access_token=new_access_token)