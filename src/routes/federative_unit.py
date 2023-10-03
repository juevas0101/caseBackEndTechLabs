from flask import Blueprint, jsonify, request
from ..models import db, FederativeUnit

federative_unit_bp = Blueprint('federative_unit', __name__)

@federative_unit_bp.route('/federative_unit', methods=['GET'])
def list_all_federative_units():
    federative_units = FederativeUnit.query.all()
    federative_unit_list = [{
        "id": federative_unit.id,
        "name_state": federative_unit.name_state
    } for federative_unit in federative_units]
    return jsonify({"federative_units": federative_unit_list})


@federative_unit_bp.route('/federative_unit', methods=['POST'])
def create_federative_unit():
    data = request.get_json()

    required_fields = ["name_state"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "All required fields (name_state) must be provided"}), 400

    try:
        new_federative_unit = FederativeUnit(
            name_state=data["name_state"]
        )

        db.session.add(new_federative_unit)
        db.session.commit()

        return jsonify({"message": "FederativeUnit created successfully"}), 201

    except Exception as e:
        db.session.rollback(e)
        return jsonify({"error": "An error occurred while creating the FederativeUnit"}), 500
    

@federative_unit_bp.route('/federative_unit/<int:id>', methods=['PUT'])
def update_federative_unit(id):
    data = request.get_json()

    federative_unit = FederativeUnit.query.get(id)
    if not federative_unit:
        return jsonify({"error": "FederativeUnit not found"}), 404

    try:
        if "name_state" in data:
            federative_unit.name_state = data["name_state"]

        db.session.commit()

        return jsonify({"message": "FederativeUnit updated successfully"}), 200

    except Exception as e:
        db.session.rollback(e)
        return jsonify({"error": "An error occurred while updating the FederativeUnit"}), 500
    

@federative_unit_bp.route('/federative_unit/<int:id>', methods=['DELETE'])
def delete_federative_unit(id):
    federative_unit_to_delete = FederativeUnit.query.get(id)
    if not federative_unit_to_delete:
        return jsonify({"error": "FederativeUnit not found"}), 404

    try:
        db.session.delete(federative_unit_to_delete)
        db.session.commit()

        return jsonify({"message": "FederativeUnit deleted successfully"}), 200

    except Exception as e:
        db.session.rollback(e)
        return jsonify({"error": "An error occurred while deleting the FederativeUnit"}), 500
