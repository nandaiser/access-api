from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, User
from werkzeug.security import generate_password_hash, check_password_hash

user_bp = Blueprint('user', __name__)

@user_bp.route("/settings", methods=["PUT", "DELETE"])
@jwt_required()
def user_config():
    data = request.get_json()
    user_id = data.get("id")
    user_pass = data.get("password")

    if not user_id or not user_pass:
        return jsonify({"error": "ID or password required"}), 400
    
    current_user = get_jwt_identity()
    if current_user != user_id:
        return jsonify({"error": "Unauthorized action"}), 403
    
    listed_user = User.query.get(user_id)
    if not listed_user:
        return jsonify({"error": "User not found"}), 404
    
    if not check_password_hash(listed_user.password, user_pass):
        return jsonify({"error": "Wrong password"}), 401
    
    if request.method == "PUT":
        new_password = data.get("new_password","").strip()
        if len(new_password) <= 6:
            return jsonify({"error": "New password must be at least 6 characters"}), 400
        if not new_password:
            return jsonify({"error": "New password required"}), 400
        
        listed_user.password = generate_password_hash(new_password)
        db.session.commit()
        return jsonify({"message": "Password updated successfully"}), 200

    elif request.method == "DELETE":
        db.session.delete(listed_user)
        db.session.commit()
        return jsonify({"message": f"User '{user_id}' deleted"}), 200

@user_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    current_user = get_jwt_identity()
    return jsonify(message=f"Welcome {current_user}")