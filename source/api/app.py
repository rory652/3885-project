import redis as redis
from flask import Flask, session, request
from flask_restful import Api, Resource
from flask_session import Session
from os import getenv
from dotenv import load_dotenv

from databases.users import Users
from databases.contacts import Contacts
from databases.residents import Residents
from databases.modules import Modules

load_dotenv()
APP_KEY = getenv('APP_KEY')
SESSION_PASS = getenv('SESSION_PASS')
DB_PASS = getenv('DB_PASS')

app = Flask(__name__)
api = Api(app)

# Details on the Secret Key: https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY
# NOTE: The secret key is used to cryptographically-sign the cookies used for storing
#       the session identifier.
app.secret_key = APP_KEY

# Configure Redis for storing the session data on the server-side
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_REDIS'] = redis.Redis(host="session", port=6379, password=SESSION_PASS)

# Create and initialize the Flask-Session object AFTER `app` has been configured
server_session = Session(app)

# Different database objects
userDB = Users(DB_PASS)
contactDB = Contacts(DB_PASS)
residentDB = Residents(DB_PASS)
moduleDB = Modules(DB_PASS)

# Permissions:
#   0 - Resident
#   1 - Nurse
#   2 - Admin
#   -1 - Module
PERMISSIONS = {"resident": 0, "nurse": 1, "admin": 2, "module": -1}


class Contact(Resource):
    def delete(self, contact_id):
        if "username" not in session:
            return "user not logged in", 401

        if session.get("permissions") < PERMISSIONS["nurse"]:
            return "invalid credentials", 403

        contactDB.delete(contact_id)
        return '', 204


class Contacts(Resource):
    def get(self):
        if "username" not in session:
            return "user not logged in", 401

        if session.get("permissions") < PERMISSIONS["nurse"]:
            return "invalid credentials", 403

        return contactDB.get()


class Module(Resource):
    def get(self, module_id):
        if "username" not in session:
            return "no user logged in", 401

        if session.get("permissions") < PERMISSIONS["admin"]:
            return 'invalid user', 403

        return moduleDB.get(module_id)

    def put(self, module_id):
        if "username" not in session:
            return "no user logged in", 401

        if not session.get("permissions") == PERMISSIONS["module"]:
            return "invalid user", 403

        args = request.get_json(force=True)

        newInfo = moduleDB.update(module_id, args["new-status"], args["new-room"])
        if newInfo is None:
            return "field not set", 400

        return newInfo, 201

    def delete(self, module_id):
        if "username" not in session:
            return "user not logged in", 401

        if session.get("permissions") < PERMISSIONS["admin"]:
            return "invalid credentials", 403

        contactDB.delete(module_id)
        return '', 204


class Modules(Resource):
    def get(self):
        if "username" not in session:
            return "user not logged in", 401

        if session.get("permissions") < PERMISSIONS["admin"]:
            return "invalid credentials", 403

        return moduleDB.get()

    def post(self):
        if "username" not in session:
            return "user not logged in", 401

        if session.get("permissions") < PERMISSIONS["admin"]:
            return "invalid credentials", 403

        args = request.get_json(force=True)

        if not moduleDB.add(args["room"], args["status"]):
            return "failed to add resident", 400

        return "module added", 201


class Resident(Resource):
    def get(self, resident_id):
        if "username" not in session:
            return "no user logged in", 401

        if session.get("permissions") < PERMISSIONS["nurse"]:
            return 'invalid user', 403

        return residentDB.get(resident_id)

    def put(self, resident_id):
        if "username" not in session:
            return "no user logged in", 401

        if not session.get("permissions") < PERMISSIONS["nurse"]:
            return "invalid user", 403

        args = request.get_json(force=True)

        newInfo = residentDB.update(resident_id, args["new-name"], args["new-wearable"], args["new-status"])
        if newInfo is None:
            return "field not set", 400

        return "resident updated", 201

    def delete(self, resident_id):
        if "username" not in session:
            return "user not logged in", 401

        if session.get("permissions") < PERMISSIONS["nurse"]:
            return "invalid credentials", 403

        contactDB.delete(resident_id)
        return '', 204


class Residents(Resource):
    def get(self):
        if "username" not in session:
            return "user not logged in", 401

        if session.get("permissions") < PERMISSIONS["nurse"]:
            return "invalid credentials", 403

        return residentDB.get()

    def post(self):
        if "username" not in session:
            return "user not logged in", 401

        if session.get("permissions") < PERMISSIONS["nurse"]:
            return "invalid credentials", 403

        args = request.get_json(force=True)

        if not residentDB.add(args["name"], args["wearable"], args["status"]):
            return "failed to add resident", 400

        return "resident added", 201


class User(Resource):
    def get(self, username):
        if not userDB.contains(username):
            return "resource not found", 404

        if "username" not in session:
            return "no user logged in", 401

        if not session.get("username") == username:
            return "invalid user", 403

        return userDB.get(username)

    def put(self, username):
        if not userDB.contains(username):
            return "resource not found", 404

        if "username" not in session:
            return "no user logged in", 401

        if not session.get("username") == username:
            return "invalid user", 403

        args = request.get_json(force=True)

        # Verify that the user is legitimate
        if not userDB.verify(args["username"], args["password"]):
            return "invalid credentials", 400

        if "new-username" not in args:
            args["new-username"] = None

        if "new-password" not in args:
            args["new-password"] = None

        newUsername, newInfo = userDB.update(args["username"], args["new-username"], args["new-password"])
        if newInfo is None:
            return "field not set", 400

        # Update session
        session['username'] = newUsername
        session['permissions'] = newInfo["permissions"]
        return "user updated", 201

    def delete(self, username):
        if not userDB.contains(username):
            return "resource not found", 404

        if "username" not in session:
            return "no user logged in", 401

        if not session.get("username") == username:
            return "invalid user", 403

        userDB.delete(username)

        # Delete the session
        session.pop('username', default=None)
        session.pop('permissions', default=None)
        return '', 204


class Users(Resource):
    def get(self):
        if "username" not in session:
            return "user not logged in", 401

        if session.get("permissions") < PERMISSIONS["admin"]:
            return "invalid credentials", 403

        return userDB.get()

    def post(self):
        args = request.get_json(force=True)

        permissions = 0
        if "permissions" in args:
            permissions = args["permissions"]

        if not userDB.add(args["username"], args["password"], permissions):
            return "failed to add user", 400

        # Create a session
        session['username'] = args["username"]
        session['permissions'] = permissions
        return "user added", 201


class UserSession(Resource):
    def post(self):
        args = request.get_json(force=True)

        if userDB.verify(args["username"], args["password"]):
            session['username'] = args["username"]
            session['permissions'] = userDB.get(args["username"])["permissions"]

            return "session created", 201

        return "invalid login credentials", 400

    def delete(self):
        session.pop('username', default=None)
        session.pop('permissions', default=None)

        return '', 204


api.add_resource(Contacts, '/contacts/')
api.add_resource(Contact, '/contacts/<contact_id>')

api.add_resource(Modules, '/modules/')
api.add_resource(Module, '/modules/<module_id>')

api.add_resource(Residents, '/residents/')
api.add_resource(Resident, '/residents/<resident_id>')

api.add_resource(Users, '/users/')
api.add_resource(User, '/users/<username>')

api.add_resource(UserSession, '/login/')
