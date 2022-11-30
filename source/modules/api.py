from flask_restful import Resource


class Module(Resource):
    def get(self, module_id):
        return {'page': 'module get'}

    def put(self, module_id):
        return {'page': 'module put'}, 201

    def delete(self, module_id):
        return '', 204


class Modules(Resource):
    def get(self):
        return {'page': 'modules get'}

    def post(self):
        return {'page': 'modules post'}, 201
