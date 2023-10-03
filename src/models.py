from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class People(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    cpf = db.Column(db.String(11), nullable=False, unique=True)
    marital_status = db.Column(db.String(20))
    email = db.Column(db.String(100), nullable=False, unique=True)
    birth_date = db.Column(db.Date, nullable=False)

    departament_id = db.Column(db.Integer, db.ForeignKey('departament.id'))
    departament = db.relationship('Departament', back_populates='people')

    telephone_id = db.Column(db.Integer, db.ForeignKey('telephone.id'))
    telephone = db.relationship('Telephone', back_populates='people')

    address_id = db.Column(db.Integer, db.ForeignKey('address.id'))
    address = db.relationship('Address', back_populates='people')

class Departament(db.Model):
    __tablename__ = 'departament'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name_departament = db.Column(db.String(100), nullable=False, unique=True)
    employees = db.Column(db.Integer, nullable=False)
    
    people = db.relationship('People', back_populates='departament')
    
class Address(db.Model):
    __tablename__ = 'address'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_place = db.Column(db.String(100), nullable=False, unique=True)
    neighborhood = db.Column(db.String(100), nullable=False, unique=True)
    people = db.relationship('People', back_populates='address')

    federative_unit_id = db.Column(db.Integer, db.ForeignKey('federative_unit.id'))
    federative_unit = db.relationship('FederativeUnit', back_populates='address')

class Telephone(db.Model):
    __tablename__ = 'telephone'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    telephone_number = db.Column(db.String(10), nullable=False, unique=True)
    telephone_house = db.Column(db.String(100), nullable=False, unique=True)
    
    people = db.relationship('People', back_populates='telephone')

class FederativeUnit(db.Model):
    __tablename__ = 'federative_unit'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name_state = db.Column(db.String(2), nullable=False, unique=True)

    address = db.relationship('Address', back_populates='federative_unit')
