from flask import Flask
from flask_restful import Api

# Import the different sections of the API
from contacts.api import Contacts
from modules.api import Modules
from residents.api import Residents
from users.api import Users

app = Flask(__name__)
api = Api(app)

api.add_resource(Contacts, '/contacts/')
api.add_resource(Modules, '/modules/')
api.add_resource(Residents, '/residents/')
api.add_resource(Users, '/users/')

if __name__ == '__main__':
    app.run(debug=True)
