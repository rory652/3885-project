from flask_restful import Resource


class Residents(Resource):
    def get(self):
        return {'page': 'residents'}
