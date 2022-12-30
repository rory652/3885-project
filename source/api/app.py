import redis as redis
from flask import Flask, session, request
from flask_restful import Api, Resource
from flask_session import Session
from os import getenv
from dotenv import load_dotenv

import users

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
userDB = users.Users(DB_PASS)


class User(Resource):
    def get(self, username):
        if session.get("username") == username:
            userDB.get(username)
        return {"user": username}

    def put(self, username):
        if "username" not in session:
            return "no user logged in", 401

        if not session.get("username") == username:
            return "invalid user", 403

        args = request.get_json(force=True)

        # Verify that the user is legitimate
        if not userDB.verify(args["username"], args["password"]):
            return "invalid credentials", 400

        newInfo = userDB.update(args["username"], args["new-username"], args["new-password"])
        if newInfo is None:
            return "field not set", 400

        # Update session
        session['username'] = newInfo["username"]
        session['permissions'] = newInfo["permissions"]
        return "user updated", 201

    def delete(self, username):
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

        if session.get("permissions") < 3:
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


api.add_resource(Users, '/users/')
api.add_resource(User, '/users/<username>')
api.add_resource(UserSession, '/login/')
