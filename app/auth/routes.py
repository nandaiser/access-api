from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required
from app.models import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/home", methods=["POST"])
def login():
    data = request.get_json()
    user_id = data.get("id")
    user_pass = data.get("password")
    
    if not user_id or not user_pass:
        abort(400, description="ID or PASS cannot be empty")
        
    listed_user = User.query.get(user_id)
    
    if listed_user and listed_user.password == user_pass:
        access_token = create_access_token(identity=user_id)
        refresh_token = create_refresh_token(identity=user_id)
        return jsonify({
            "Successful login": f"Welcome back {user_id}",
            "access token": access_token,
            "refresh token": refresh_token
        }), 200
    
    if listed_user:
        return jsonify({"error": "Wrong password"}), 401
    
    return jsonify({"User not in database": "Please sign up"}), 404

@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    user_id = data.get("id")
    user_pass = data.get("password")
    
    if not user_id or not user_pass:
        return jsonify({"error": "ID and password required"}), 400
    
    listed_user = User.query.get(user_id)
    if listed_user:
        return jsonify({"error": "You already have an account. Try to log in."}), 409
    
    new_user = User(id=user_id, password=user_pass)
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