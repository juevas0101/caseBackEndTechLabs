from flask import Blueprint, jsonify, request
from ..models import db, Telephone

telephone_bp = Blueprint('telephone', __name__)

@telephone_bp.route('/telephone', methods=['GET'])
def list_all_telephones():
    telephones = Telephone.query.all()
    telephone_list = [{
        "id": telephone.id,
        "personal_phone": telephone.personal_phone,
        "home_phone": telephone.home_phone
    } for telephone in telephones]
    return jsonify({"telephones": telephone_list})


@telephone_bp.route('/telephone', methods=['POST'])
def create_telephone():
    data = request.get_json()

    required_fields = ["personal_phone", "home_phone"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "All required fields (personal_phone, home_phone) must be provided"}), 400

    try:
        new_telephone = Telephone(
            personal_phone=data["personal_phone"],
            home_phone=data["home_phone"]
        )

        db.session.add(new_telephone)
        db.session.commit()

        return jsonify({"message": "Telephone created successfully"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred while creating the telephone"}), 500
    

@telephone_bp.route('/telephone/<int:id>', methods=['PATCH', 'PUT'])
def update_telephone(id):
    data = request.get_json()

    telephone = Telephone.query.get(id)
    if not telephone:
        return jsonify({"error": "Telephone not found"}), 404

    try:
        if request.method == 'PATCH':
            if "personal_phone" in data:
                telephone.personal_phone = data["personal_phone"]
            if "home_phone" in data:
                telephone.home_phone = data["home_phone"]
        elif request.method == 'PUT':
            if "personal_phone" in data:
                telephone.personal_phone = data["personal_phone"]
            if "home_phone" in data:
                telephone.home_phone = data["home_phone"]

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
