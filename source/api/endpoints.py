from flask import Flask, session, request
from flask_restful import Api, Resource

import databases.users as users
import databases.contacts as contacts
import databases.residents as residents
import databases.modules as modules
import databases.locations as locations

# Different database objects
userDB = None
contactDB = None
locationDB = None
residentDB = None
moduleDB = None

# Permissions:
#   0 - Resident
#   1 - Nurse
#   2 - Admin
#   -1 - Module
PERMISSIONS = {"resident": 0, "nurse": 1, "admin": 2, "module": -1}


def initialiseDB(password):
    global userDB, contactDB, locationDB, residentDB, moduleDB

    userDB = users.Users(password)
    contactDB = contacts.Contacts(password)
    locationDB = locations.Locations(password)
    residentDB = residents.Residents(password)
    moduleDB = modules.Modules(password)


# Just checks if a value is set, not if the argument itself is valid
def checkArgs(arguments, keys):
    for key in keys:
        if key not in arguments:
            return f"{key} not set", 400

    return False


def validateUser(userSession, permission, carehome=None):
    if "username" not in userSession:
        return "user not logged in", 401

    if userSession.get("permissions") < permission:
        return "invalid credentials", 403

    if userSession.get("carehome") != carehome and carehome is not None:
        return "user not a member of carehome", 403

    return False


class Contact(Resource):
    def delete(self, carehome, contact_id):
        if not contactDB.contains(contact_id):
            return "resource not found", 404

        if toReturn := validateUser(session, PERMISSIONS["nurse"], carehome):
            return toReturn

        contactDB.delete(contact_id)
        return '', 204


class Contacts(Resource):
    def get(self, carehome):
        if toReturn := validateUser(session, PERMISSIONS["nurse"], carehome):
            return toReturn

        return contactDB.get(carehome)


class Locations(Resource):
    def post(self, carehome):
        if "username" not in session:
            return "user not logged in", 401

        if not session.get("permissions") == PERMISSIONS["module"]:
            return "invalid credentials", 403

        if session.get("carehome") != carehome and carehome is not None:
            return "user not a member of carehome", 403

        args = request.get_json(force=True)

        if toReturn := checkArgs(args, ["wearable", "coordinates"]):
            return toReturn

        return locationDB.add(session.get("username"), args["wearable"], str(args["coordinates"]), carehome)


class Module(Resource):
    def get(self, carehome, module_id):
        if not moduleDB.contains(module_id):
            return "resource not found", 404

        if toReturn := validateUser(session, PERMISSIONS["admin"], carehome):
            return toReturn

        return moduleDB.get(carehome, module_id)

    def put(self, carehome, module_id):
        if not moduleDB.contains(module_id):
            return "resource not found", 404

        if "username" not in session:
            return "no user logged in", 401

        if not session.get("permissions") == PERMISSIONS["module"]:
            return "invalid user", 403

        if session.get("carehome") != carehome and carehome is not None:
            return "user not a member of carehome", 403

        args = request.get_json(force=True)

        if toReturn := checkArgs(args, ["new-status", "new-room"]):
            return toReturn

        newInfo = moduleDB.update(module_id, carehome, args["new-status"], args["new-room"])
        if newInfo is None:
            return "field not set", 400

        return newInfo, 201

    def delete(self, carehome, module_id):
        if not moduleDB.contains(module_id):
            return "resource not found", 404

        if toReturn := validateUser(session, PERMISSIONS["admin"], carehome):
            return toReturn

        moduleDB.delete(module_id)
        return '', 204


class Modules(Resource):
    def get(self, carehome):
        if toReturn := validateUser(session, PERMISSIONS["admin"], carehome):
            return toReturn

        return moduleDB.get(carehome)

    def post(self, carehome):
        if toReturn := validateUser(session, PERMISSIONS["admin"], carehome):
            return toReturn

        args = request.get_json(force=True)

        if toReturn := checkArgs(args, ["status", "room"]):
            return toReturn

        return moduleDB.add(args["room"], carehome, args["status"])


class Resident(Resource):
    def get(self, carehome, resident_id):
        if not residentDB.contains(resident_id):
            return "resource not found", 404

        if toReturn := validateUser(session, PERMISSIONS["nurse"], carehome):
            return toReturn

        return residentDB.get(carehome, resident_id)

    def put(self, carehome, resident_id):
        if not residentDB.contains(resident_id):
            return "resource not found", 404

        if toReturn := validateUser(session, PERMISSIONS["nurse"], carehome):
            return toReturn

        args = request.get_json(force=True)

        if toReturn := checkArgs(args, ["new-name", "new-wearable", "new-status"]):
            return toReturn

        newInfo = residentDB.update(resident_id, carehome, args["new-name"], args["new-wearable"], args["new-status"])
        if newInfo is None:
            return "field not set", 400

        return "resident updated", 201

    def delete(self, carehome, resident_id):
        if not residentDB.contains(resident_id):
            return "resource not found", 404

        if toReturn := validateUser(session, PERMISSIONS["nurse"], carehome):
            return toReturn

        residentDB.delete(resident_id)
        return '', 204


class Residents(Resource):
    def get(self, carehome):
        if toReturn := validateUser(session, PERMISSIONS["nurse"], carehome):
            return toReturn

        return residentDB.get(carehome)

    def post(self, carehome):
        if toReturn := validateUser(session, PERMISSIONS["nurse"], carehome):
            return toReturn

        args = request.get_json(force=True)

        if toReturn := checkArgs(args, ["name", "wearable", "status"]):
            return toReturn

        return residentDB.add(args["name"], args["wearable"], carehome, args["status"])


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

        if toReturn := checkArgs(args, ["username", "password", "new-username", "new-password"]):
            return toReturn

        # Verify that the user is legitimate
        if not userDB.verify(args["username"], args["password"]):
            return "invalid credentials", 400

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
        if toReturn := validateUser(session, PERMISSIONS["admin"]):
            return toReturn

        return userDB.get()

    def post(self):
        args = request.get_json(force=True)

        if toReturn := checkArgs(args, ["username", "password", "carehome", "permissions"]):
            return toReturn

        if not userDB.add(args["username"], args["password"], args["permissions"], args["carehome"]):
            return "failed to add user", 400

        # Create a session
        session['username'] = args["username"]
        session['permissions'] = args["permissions"]
        session['carehome'] = args["carehome"]

        return "user added", 201


class UserSession(Resource):
    def post(self):
        args = request.get_json(force=True)

        if toReturn := checkArgs(args, ["username", "password"]):
            return toReturn

        if userDB.verify(args["username"], args["password"]):
            session['username'] = args["username"]
            session['permissions'] = userDB.get(args["username"])["permissions"]
            session['carehome'] = userDB.get(args["username"])["carehome"]

            return "session created", 201

        return "invalid login credentials", 400

    def delete(self):
        args = request.get_json(force=True)

        if toReturn := checkArgs(args, ["username", "password"]):
            return toReturn

        if userDB.verify(args["username"], args["password"]):
            session.pop('username', default=None)
            session.pop('permissions', default=None)
            session.pop('carehome', default=None)

            return '', 204
        return "invalid login credentials", 400