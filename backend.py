from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class Key(Resource):
    def get(self):
        args = request.args
        return {'key': args['k'], 'length': len(args['k'])}, 200
    pass

api.add_resource(Key, '/key')

if __name__ == '__main__':
    app.run()