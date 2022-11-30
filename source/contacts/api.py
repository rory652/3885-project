from flask_restful import Resource


class Contact(Resource):
    def delete(self, contact_id):
        return '', 204


class Contacts(Resource):
    def get(self):
        return {'page': 'contacts get'}
