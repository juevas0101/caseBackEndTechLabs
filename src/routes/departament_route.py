from flask import Blueprint, jsonify, request
from ..models import db, Departament

departament_bp = Blueprint('departament', __name__)

@departament_bp.route('/departament', methods=['GET'])
def list_departament():
    departament = Departament.query.all()
    departament_list = [{
        "id": departament.id,
        "name_departament": departament.name_departament,
        "employees": departament.employees,
    } for departament in departament]
    return jsonify({"departament": departament_list})


@departament_bp.route('/departament_create', methods=['POST'])
def create_departament():
    data = request.get_json()

    required_fields = ["name_departament", "employees"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "All required fields (name_departament, employees) must be provided"}), 400
    
    try:
        new_departament = Departament(
            name_departament=data["name_departament"],
            employees=0
        )
        
        db.session.add(new_departament)
        db.session.commit()

        return jsonify({"message": "Departament created successfully"}), 201
    
    except Exception as e:
        db.session.rollback(e)
        return jsonify({"error": "An error occurred while creating the departament"}), 500


@departament_bp.route('/departament/<int:id>', methods=['PUT'])
def update_departament(id):
    data = request.get_json()

    departament = Departament.query.get(id)
    if not departament:
        return jsonify({"error": "Departament not found"}), 404

    try:
        if "name_departament" in data:
            departament.name_departament = data["name_departament"]
        if "employees" in data:
            departament.employees = data["employees"]

        db.session.commit()

        return jsonify({"message": "Departament updated successfully"}), 200

    except Exception as e:
        db.session.rollback(e)
        return jsonify({"error": "An error occurred while updating the departament"}), 500
    

@departament_bp.route('/departament/<int:departament>', methods=['DELETE'])
def delete_departament(departament):

    departament_to_delete = Departament.query.get(departament)
    if not departament_to_delete:
        return jsonify({"error": "departament not found"}), 404

    try:
     
        db.session.delete(departament_to_delete)
        db.session.commit()

        return jsonify({"message": "departament deleted successfully"}), 200

    except Exception as e:
        
        db.session.rollback(e)
        return jsonify({"error": "An error occurred while deleting the departament"}), 500