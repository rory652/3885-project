from flask_restful import Resource


class Contacts(Resource):
    def get(self):
        return {'page': 'contacts'}
