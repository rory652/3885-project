import redis as redis
from flask import Flask, session, request
from flask_restful import Api, Resource
from flask_session import Session
from os import getenv
from dotenv import load_dotenv

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


class User(Resource):
    def get(self, username):
        if session.get("username") == username:
            return {"user": username, "permissions": session.get("permissions")}
        return {"user": username}

    def put(self, username):
        return {'page': 'user put'}, 201

    def delete(self, username):
        return '', 204


class Users(Resource):
    def get(self):
        return {'page': 'users get'}

    def post(self):
        return {'page': 'users post'}


class UserSession(Resource):
    def post(self):
        print("hi")

        args = request.get_json(force=True)

        session['username'] = args["username"]
        session['permissions'] = args["permissions"]

        return {'page': 'users post'}, 201

    def delete(self):
        session.pop('username', default=None)
        session.pop('permissions', default=None)

        return '', 204


api.add_resource(Users, '/users/')
api.add_resource(User, '/users/<username>')
api.add_resource(UserSession, '/login/')

if __name__ == '__main__':
    app.run(debug=True)
