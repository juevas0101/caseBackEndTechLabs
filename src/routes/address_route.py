from flask import Blueprint, jsonify, request
from ..models import db, Address

address_bp = Blueprint('address', __name__)

@address_bp.route('/address', methods=['GET'])
def list_all_addresses():
    addresses = Address.query.all()
    
    address_list = [{
        "id": address.id,
        "public_place": address.public_place,
        "neighborhood": address.neighborhood,
    } for address in addresses]
    
    return jsonify({"addresses": address_list}), 200


@address_bp.route('/address_create', methods=['POST'])
def create_address():
    data = request.get_json()

    required_fields = ["public_place", "neighborhood"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "All required fields (public_place, neighborhood) must be provided"}), 400

    try:
        new_address = Address(
            public_place=data["public_place"],
            neighborhood=data["neighborhood"]
        )

        db.session.add(new_address)
        db.session.commit()

        return jsonify({"message": "Address created successfully"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred while creating the address"}), 500


@address_bp.route('/address/<int:id>', methods=['PUT'])
def update_address(id):
    data = request.get_json()

    address = Address.query.get(id)
    if not address:
        return jsonify({"error": "Address not found"}), 404

    try:
        if "public_place" in data:
            address.public_place = data["public_place"]
        if "neighborhood" in data:
            address.neighborhood = data["neighborhood"]

        db.session.commit()

        return jsonify({"message": "Address updated successfully"}), 200

    except Exception as e:
        db.session.rollback(e)
        return jsonify({"error": "An error occurred while updating the address"}), 500
    

@address_bp.route('/address/<int:address>', methods=['DELETE'])
def delete_address(address):

    address_to_delete = Address.query.get(address)
    if not address_to_delete:
        return jsonify({"error": "Address not found"}), 404

    try:
     
        db.session.delete(address_to_delete)
        db.session.commit()

        return jsonify({"message": "Address deleted successfully"}), 200

    except Exception as e:
        
        db.session.rollback(e)
        return jsonify({"error": "An error occurred while deleting the address"}), 500
