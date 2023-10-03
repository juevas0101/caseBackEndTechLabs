from flask import Blueprint, jsonify, request
from ..models import db, Telephone

telephone_bp = Blueprint('telephone', __name__)

@telephone_bp.route('/telephone', methods=['GET'])
def list_all_telephones():
    telephones = Telephone.query.all()
    telephone_list = [{
        "id": telephone.id,
        "telephone_number": telephone.telephone_number,
        "telephone_house": telephone.telephone_house
    } for telephone in telephones]
    return jsonify({"telephones": telephone_list})


@telephone_bp.route('/telephone', methods=['POST'])
def create_telephone():
    data = request.get_json()

    required_fields = ["telephone_number", "telephone_house"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "All required fields (telephone_number, telephone_house) must be provided"}), 400

    try:
        new_telephone = Telephone(
            telephone_number=data["telephone_number"],
            telephone_house=data["telephone_house"]
        )

        db.session.add(new_telephone)
        db.session.commit()

        return jsonify({"message": "Telephone created successfully"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred while creating the telephone"}), 500
    

@telephone_bp.route('/telephone/<int:id>', methods=['PUT'])
def update_telephone(id):
    data = request.get_json()

    telephone = Telephone.query.get(id)
    if not telephone:
        return jsonify({"error": "Telephone not found"}), 404

    try:
        if "telephone_number" in data:
            telephone.telephone_number = data["telephone_number"]
        if "telephone_house" in data:
            telephone.telephone_house = data["telephone_house"]

        db.session.commit()

        return jsonify({"message": "Telephone updated successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred while updating the telephone"}), 500
    

@telephone_bp.route('/telephone/<int:telephone>', methods=['DELETE'])
def delete_telephone(telephone):
    telephone_to_delete = Telephone.query.get(telephone)
    if not telephone_to_delete:
        return jsonify({"error": "Telephone not found"}), 404

    try:
        db.session.delete(telephone_to_delete)
        db.session.commit()

        return jsonify({"message": "Telephone deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred while deleting the telephone"}), 500
