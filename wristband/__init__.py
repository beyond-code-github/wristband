from flask import Flask
from flask_restful import Resource, Api
import types
import json
import requests

app = Flask(__name__)
api = Api(app)

releases_endpoint = "https://releases.tax.service.gov.uk"


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


@api.route('/api/versions/<deploy_env>/<app_name>')
class EnvVersions(Resource):
    def get(self, deploy_env, app_name):
        all_apps = requests.get('{}/apps'.format(releases_endpoint)).json()
        app_versions = [x['ver'] for x in all_apps if deploy_env == x['env'] and app_name in x['an']]
        if app_versions:
            return {'versions': app_versions}
        else:
            return {}, 404
        #return all_apps


#@FLASK_APP.route('/api/promote/<deploy_env>/<app_name>/<app_version>',
#                 methods=['POST'])
#def promote_version(deploy_env, app_name, app_version):
#    jenkins = Jenkins(deploy_env=deploy_env, auth=ldap_credentials())
#    return jsonify(jenkins.promote(app_name, app_version))
#
#
#@FLASK_APP.route('/api/build/<deploy_env>/<queue_id>', methods=['GET'])
#def promote_build_id(deploy_env, queue_id):
#    jenkins = Jenkins(deploy_env=deploy_env, auth=ldap_credentials())
#    return jsonify(jenkins.build_id(queue_id))
#
#
#@FLASK_APP.route('/api/progress/<deploy_env>/<build_id>', methods=['GET'])
#def promote_progress(deploy_env, build_id):
#    jenkins = Jenkins(deploy_env=deploy_env, auth=ldap_credentials())
#    return jsonify(jenkins.progress(build_id))




if __name__ == '__main__':
    import os
    app.run(debug=True, port=int(os.getenv("PORT", "5000")))
