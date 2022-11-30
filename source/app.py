from flask import Flask
from flask_restful import Api

# Import the different sections of the API
from contacts.api import Contacts, Contact
from modules.api import Modules, Module
from residents.api import Residents, Resident
from users.api import Users, User

app = Flask(__name__)
api = Api(app)

api.add_resource(Contacts, '/contacts/')
api.add_resource(Contact, '/contacts/<contact_id>')

api.add_resource(Modules, '/modules/')
api.add_resource(Module, '/modules/<module_id>')

api.add_resource(Residents, '/residents/')
api.add_resource(Resident, '/residents/<resident_id>')

api.add_resource(Users, '/users/')
api.add_resource(User, '/users/<user_id>')

if __name__ == '__main__':
    app.run(debug=True)
