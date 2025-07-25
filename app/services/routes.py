from flask import Blueprint,request, jsonify, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash
from app.models import Service, db

services_bp = Blueprint("services",__name__)

@services_bp.route("/manage", methods = ["POST","GET","DELETE"])
@jwt_required()
def services():
    current_user = get_jwt_identity()
    service = Service.query.get(service_id)
    
    if service_id is None or service.owner_id != current_user :
        return jsonify({"error": "Service not found or unauthorized"}), 404
    
    if request.method == "POST":
        data = request.get_json()
        title = data.get("service","").strip()
        price = data.get("price")
        description = data.get("description","").strip()

        if not title or price is None:
            return jsonify({"error": "Service and price are required"}), 400
        
        new_service = Service(
            service = title,
            price = price,
            description = description,
            owner_id = current_user)
        
        db.session.add(new_service)
        db.session.commit()
        
        return jsonify({"message": "Service created", "service_id": new_service.id}), 201

    elif request.method == "GET":
        user_services = Service.query.filter_by(owner_id = current_user).all()
        result = [
            {
                "id": svc.id,
                "service": svc.service,
                "price": svc.price,
                "description": svc.description
            } for svc in user_services
        ]
        if len(result) == 0:
            return jsonify({"message" : "service not found"}), 404
        
        return jsonify(result), 200
    
    elif request.method == "DELETE":
        data = request.get_json()
        service_id = data.get("id")
        
        if not service_id:
            return jsonify({"error": "Service ID is required"}), 400
        
        service = Service.query.get(service_id)
        if service_id is None or service.owner_id != current_user :
            return jsonify({"error": "Service not found or unauthorized"}), 404
        
        db.session.delete(service)
        db.session.commit()
        
        return jsonify({"message": f"service '{service_id}' {service.service} , by {service.owner_id} has been deleted "})
        