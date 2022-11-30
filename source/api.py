from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class Contacts(Resource):
    def get(self):
        return {'page': 'contacts'}


class Modules(Resource):
    def get(self):
        return {'page': 'modules'}


class Residents(Resource):
    def get(self):
        return {'page': 'residents'}


class Users(Resource):
    def get(self):
        return {'page': 'users'}


api.add_resource(Contacts, '/contacts/')
api.add_resource(Modules, '/modules/')
api.add_resource(Residents, '/residents/')
api.add_resource(Users, '/users/')

if __name__ == '__main__':
    app.run(debug=True)
