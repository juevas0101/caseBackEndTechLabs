from flask import Blueprint, jsonify, request
from ..models import db, People, Departament, Address, Telephone

people_bp = Blueprint('people', __name__)

@people_bp.route('/people', methods=['GET'])
def list_all_people():
    people = People.query.all()
    people_list = [{
        "id": people.id,
        "first_name": people.first_name,
        "last_name": people.last_name,
        "cpf": people.cpf,
        "marital_status": people.marital_status,
        "email": people.email,
        "birth_date": people.birth_date.strftime('%Y-%m-%d'),
        "departament_id": people.departament_id,  
        "address_id": people.address_id, 
        "telephone_id": people.telephone_id
    } for people in people]
    return jsonify({"people": people_list})


@people_bp.route('/people', methods=['POST'])
def create_people():
    data = request.get_json()

    required_fields = ["first_name", "last_name", "cpf", "marital_status", "email", "birth_date", "departament_id",  "address_id", "telephone_id"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "All required fields must be provided"}), 400

    try:
        new_people = People(
            first_name=data["first_name"],
            last_name=data["last_name"],
            cpf=data["cpf"],
            marital_status=data.get("marital_status"),
            email=data["email"],
            birth_date=data["birth_date"],
            departament_id=data["departament_id"],
            address_id=data["address_id"],
            telephone_id=data["telephone_id"]
        )

        address = Address.query.get(data.get("address_id"))
        telephone = Telephone.query.get(data.get("telephone_id"))
        departament = Departament.query.get(data["departament_id"])

        if address:
            new_people.address = address
        if telephone:
            new_people.telephone = telephone
        if departament:
            departament.employees += 1

        db.session.add(new_people)
        db.session.commit()

        return jsonify({"message": "People created successfully"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred while creating the people: {str(e)}"}), 500
    

@people_bp.route('/people/<int:id>', methods=['PATCH', 'PUT'])
def update_people(id):
    data = request.get_json()

    people = People.query.get(id)
    if not people:
        return jsonify({"error": "people not found"}), 404

    try:
        if request.method == 'PATCH':
            if "first_name" in data:
                people.first_name = data["first_name"]
            if "last_name" in data:
                people.last_name = data["last_name"]
            if "cpf" in data:
                people.cpf = data["cpf"]
            if "marital_status" in data:
                people.marital_status = data["marital_status"]
            if "email" in data:
                people.email = data["email"]
            if "birth_date" in data:
                people.birth_date = data["birth_date"]

        elif request.method == 'PUT':
            if "first_name" in data:
                people.first_name = data["first_name"]
            if "last_name" in data:
                people.last_name = data["last_name"]
            if "cpf" in data:
                people.cpf = data["cpf"]
            if "marital_status" in data:
                people.marital_status = data["marital_status"]
            if "email" in data:
                people.email = data["email"]
            if "birth_date" in data:
                people.birth_date = data["birth_date"]

            db.session.commit()

        return jsonify({"message": "people updated successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred while updating the people"}), 500
    

@people_bp.route('/people/<int:people>', methods=['DELETE'])
def delete_people(people):

    people_to_delete = People.query.get(people)
    if not people_to_delete:
        return jsonify({"error": "People not found"}), 404

    try:
     
        db.session.delete(people_to_delete)
        db.session.commit()

        return jsonify({"message": "People deleted successfully"}), 200

    except Exception as e:
        
        db.session.rollback()
        return jsonify({"error": "An error occurred while deleting the people"}), 500
    