from flask import Flask, Response
from flask_restful import Resource, Api
import types
import json
import requests
from jenkinsapi.jenkins import Jenkins
from urlparse import urlparse

app = Flask(__name__)
api = Api(app)

app.config.from_envvar("CONFIG_FILE", "config/production.py")
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
        envs = {
            'envs': {
                'QA': [
                    'qa-left',
                    'qa-right'
                ],
                'Staging': [
                    'staging-left',
                    'staging-right'
                ]
            },
        }
        #'apps': Releases().apps()
        return envs


@api.route('/api/versions/<deploy_env>/<app_name>')
class EnvVersionsResource(Resource):
    def get(self, deploy_env, app_name):
        sorted_app_versions = [x['ver'] for x in get_all_releases() if deploy_env == x['env'] and app_name == x['an']]
        if sorted_app_versions:
            return {'versions': sorted_app_versions}
        else:
            return {}, 404

def get_all_releases():
    return requests.get('{}/apps'.format(releases_endpoint)).json()


def sse(event, data):
    return "".join([
        "event: {}\n".format(event),
        "data: {}\n\n".format(str(data))
    ])

@api.route('/api/promote/<deploy_env>/<app_name>/<app_version>')
class Promotions(Resource):
    def post(self, deploy_env, app_name, app_version):
        # Hardcoded for speed !!!!
        pipeline = app.config.get('PIPELINES')[deploy_env.split("-")[1]]
        pipeline_position = pipeline.index(deploy_env)

        if pipeline_position != 0:
            # We're not the first environment in the pipeline, check previous
            releases = get_all_releases()
            app_version_in_environments = [r["env"] for r in releases if r["an"] == app_name and r["ver"] == app_version]
            if pipeline[pipeline_position -1] not in app_version_in_environments:
                return {"error": "you need to deploy {} to {} first".format(app_version, pipeline[pipeline_position -1])}, 400

        jenkins_uri = app.config['ENVIRONMENTS'][deploy_env]["jenkins_uri"]
        parsed_jenkins_uri = urlparse(jenkins_uri)
        # Very hacky
        jenkins = Jenkins(jenkins_uri.replace("{}:{}@".format(parsed_jenkins_uri.username, parsed_jenkins_uri.password), ""), username=parsed_jenkins_uri.username, password=parsed_jenkins_uri.password)
        dm = jenkins.get_job("deploy-microservice")
        params = {"APP": app_name, "APP_BUILD_NUMBER": app_version}
        running_job = dm.invoke(build_params=params, securitytoken=None)
        def gen():
            yield sse("message", "queued")
            running_job.block_until_building()
            yield sse("message", "building")
            running_job.block_until_complete()
            yield sse("message", "success" if running_job.is_good() else "failed")
        return Response(gen(), content_type="text/event-stream")


if __name__ == '__main__':
    import os
    app.run(debug=True, port=int(os.getenv("PORT", "5000")))
