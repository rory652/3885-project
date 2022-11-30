from flask_restful import Resource


class Modules(Resource):
    def get(self):
        return {'page': 'modules'}
