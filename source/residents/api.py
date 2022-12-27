from flask_restful import Resource


class Resident(Resource):
    def get(self, resident_id):
        return {'page': 'resident get'}

    def put(self, resident_id):
        return {'page': 'resident put'}, 201

    def delete(self, resident_id):
        return '', 204


class Residents(Resource):
    def get(self):
        return {'page': 'residents get'}

    def post(self):
        return {'page': 'residents post'}
