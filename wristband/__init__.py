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


def get_all_releases():
    data = requests.get('{}/apps'.format(releases_endpoint)).json()
    return data


def get_all_releases_of_app_in_env(deploy_env, app_name, releases):
    releases_for_env = []
    for release in releases:
        if deploy_env == release.get("env") and app_name == release['an']:
            del release['an']
            del release['env']
            releases_for_env.append(release)
    return sorted(releases_for_env, key=lambda k: k['ver'])#, reverse=True)


def get_all_app_names(releases):
    apps_in_environment = sorted(set([release["an"] for release in releases]))
    return apps_in_environment


def get_all_app_names_in_env(env, releases):
    apps_in_environment = sorted(set([release["an"] for release in releases if release.get("env") == env]))
    return apps_in_environment


def get_all_environments():
    pipeline_list = get_all_pipelines()
    environments = []
    for pipeline in pipeline_list:
        environments.extend(get_envs_in_pipeline(pipeline))
    return environments


def get_all_pipelines():
    return app.config.get('PIPELINES')


def get_envs_in_pipeline(pipeline):
    return app.config.get('PIPELINES')[pipeline]


def make_environment_groups(environments):
    shortenvs = sorted(set([short.split('-')[0] for short in environments]))
    envgroups = {}
    for shortenv in shortenvs:
        envgroups[shortenv] = [env for env in environments if shortenv in env]
    return envgroups


def sse(event, data):
    return "".join([
        "event: {}\n".format(event),
        "data: {}\n\n".format(str(data))
    ])


@api.route('/ping/ping')
class Ping(Resource):
    def get(self):
        return {'status': 'OK'}


@api.route('/api/config')
class APIConfig(Resource):
    def get(self):
        pipelines = get_all_pipelines()
        releases_all_envs = get_all_releases()
        environments = get_all_environments()
        envgroups = make_environment_groups(environments)
        config = {'pipelines': pipelines,
                  'envs' : envgroups }

        config["apps"] = []
        for app in get_all_app_names(releases_all_envs):
            config['apps'].append({ 'name' : app, 'envs' : {} })
            for env in environments:
                versions = get_all_releases_of_app_in_env(env, app, releases_all_envs)
                if versions:
                    config['apps'][-1]['envs'][env] = { 'versions': versions }

        if config:
            return config
        else:
            return {}, 404


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
