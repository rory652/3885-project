from flask_restful import Resource


class User(Resource):
    def get(self, user_id):
        return {'page': 'user get'}

    def put(self, user_id):
        return {'page': 'user put'}, 201

    def delete(self, user_id):
        return '', 204


class Users(Resource):
    def get(self):
        return {'page': 'users get'}

    def get(self):
        return {'page': 'users post'}
