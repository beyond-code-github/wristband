from flask import Flask
from flask_restful import Resource, Api
import types
import json

app = Flask(__name__)
api = Api(app)


def api_route(self, *args, **kwargs):
    def wrapper(cls):
        self.add_resource(cls, *args, **kwargs)
        return cls
    return wrapper

api.route = types.MethodType(api_route, api)


@api.route('/ping/ping')
class Ping(Resource):
    def get(self):
        return {'status': 'OK'}


@api.route('/api/config')
class APIConfig(Resource):
    def get(self):
        envs = json.loads(app.config.get('ENVS'))
        return envs


if __name__ == '__main__':
    import os
    app.run(debug=True, port=int(os.getenv("PORT", "5000")))
