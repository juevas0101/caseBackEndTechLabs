from flask import Flask
from flask_migrate import Migrate
from .models import db 
from .routes.people_route import people_bp
from .routes.departament_route import departament_bp
from .routes.address_route import address_bp
from .routes.telephone_route import telephone_bp
from .routes.federative_unit import federative_unit_bp

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:root@localhost/casebackend'

db.init_app(app)

app.register_blueprint(people_bp)
app.register_blueprint(departament_bp)
app.register_blueprint(address_bp)
app.register_blueprint(telephone_bp)
app.register_blueprint(federative_unit_bp)

migrate = Migrate(app, db, directory='./src/data/')

if __name__ == '__main__':
    app.run(debug=True)