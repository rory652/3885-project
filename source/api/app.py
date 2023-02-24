import redis as redis
from flask import Flask, session, request
from flask_restful import Api, Resource
from flask_session import Session
from os import getenv
from dotenv import load_dotenv

import endpoints as EP

load_dotenv()
APP_KEY = getenv('APP_KEY')
SESSION_PASS = getenv('SESSION_PASS')
DB_PASS = getenv('DB_PASS')

EP.initialiseDB(DB_PASS)

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

api.add_resource(EP.Contacts, '/contacts/<carehome>')
api.add_resource(EP.Contact, '/contacts/<carehome>/<contact_id>')

api.add_resource(EP.Locations, '/locations/<carehome>')

api.add_resource(EP.Modules, '/modules/<carehome>')
api.add_resource(EP.Module, '/modules/<carehome>/<module_id>')

api.add_resource(EP.Residents, '/residents/<carehome>')
api.add_resource(EP.Resident, '/residents/<carehome>/<resident_id>')

api.add_resource(EP.Users, '/users/')
api.add_resource(EP.User, '/users/<username>')

api.add_resource(EP.UserSession, '/login/')
