import types
from urlparse import urlparse
import os
from collections import namedtuple

from flask import Flask, Response
from flask_restful import Resource, Api
import requests
from jenkinsapi.jenkins import Jenkins

from utils import Release, Environment

app = Flask(__name__)
api = Api(app)

app.config.from_envvar("CONFIG_FILE", "config/production.py")
RELEASES_ENDPOINT = "https://releases.tax.service.gov.uk"

MessageTuple = namedtuple('MessageTuple', ['key', 'value'])

def api_route(self, *args, **kwargs):
    def wrapper(cls):
        self.add_resource(cls, *args, **kwargs)
        return cls

    return wrapper


api.route = types.MethodType(api_route, api)


def get_all_releases():
    return [Release.from_dictionary(release) for release in requests.get('{}/apps'.format(RELEASES_ENDPOINT)).json()]


def get_all_releases_of_app_in_env(deploy_env, app_name, releases):
    releases_for_env = []
    for release in releases:
        if deploy_env == release.environment and app_name == release.app_name:
            releases_for_env.append(release)
    return sorted(releases_for_env, key=lambda a: a.last_seen, reverse=True)


def get_all_app_names(releases):
    return frozenset([release.app_name for release in releases])


def get_all_app_names_in_env(env, releases):
    return frozenset([release.app_name for release in releases if release.environment == env])


def get_all_environments():
    pipeline_list = get_all_pipelines()
    environments = []
    for pipeline in pipeline_list:
        environments.append(get_envs_in_pipeline(pipeline))
    return sorted(environments)


def get_all_pipelines():
    return app.config.get('PIPELINES')


def get_envs_in_pipeline(pipeline):
    pipelines = get_all_pipelines()
    envs = None
    if pipelines:
        envs = Environment.from_environment_name(pipelines[pipeline])
    return envs


def make_environment_groups(environments):
    shortenvs = frozenset([environment.left for environment in environments])
    envgroups = {}
    for shortenv in shortenvs:
        envgroups[shortenv] = [env for env in environments if shortenv in env]
    return envgroups


def sse(messages):
    """

    :param messages: Tuple of named tuples contaning key and data
    :return:
    """
    return "".join(["{key}: {value}".format(message.key, str(message.value)) for message in messages])


@api.route('/ping/ping')
class Ping(Resource):
    def get(self):
        return {'status': 'OK'}


@api.route('/api/config')
class APIConfig(Resource):
    def get(self):
        import pdb; pdb.set_trace()
        pipelines = get_all_pipelines()
        releases_all_envs = get_all_releases()
        environments = get_all_environments()
        envgroups = make_environment_groups(environments)
        config = {'pipelines': pipelines, 'envs': envgroups, "apps": []}

        for app in get_all_app_names(releases_all_envs):
            config['apps'].append({'name': app, 'envs': {}})
            for env in environments:
                versions = get_all_releases_of_app_in_env(env, app, releases_all_envs)
                if versions:
                    config['apps'][-1]['envs'][env] = {'versions': versions}

        if config:
            return config
        else:
            return {}, 404


@api.route('/api/promote/<deploy_env>/<app_name>/<app_version>')
class Promotions(Resource):
    def get(self, deploy_env, app_name, app_version):
        pdb; pdb.set_trace()
        # Hardcoded for speed !!!!
        pipeline = app.config.get('PIPELINES')[deploy_env.split("-")[1]]
        pipeline_position = pipeline.index(deploy_env)

        if pipeline_position != 0:
            # We're not the first environment in the pipeline, check previous
            releases = get_all_releases()
            app_version_in_environments = [release.environment for release in releases if
                                           release.app_name == app_name and release.version == app_version]
            if pipeline[pipeline_position - 1] not in app_version_in_environments:
                return {"error": "you need to deploy {} to {} first".format(app_version,
                                                                            pipeline[pipeline_position - 1])}, 400

        jenkins_uri = app.config['ENVIRONMENTS'][deploy_env]["jenkins_uri"]
        parsed_jenkins_uri = urlparse(jenkins_uri)
        # Very hacky
        jenkins = Jenkins(
            jenkins_uri.replace("{}:{}@".format(parsed_jenkins_uri.username, parsed_jenkins_uri.password), ""),
            username=parsed_jenkins_uri.username, password=parsed_jenkins_uri.password)
        dm = jenkins.get_job("deploy-microservice")
        params = {"APP": app_name, "APP_BUILD_NUMBER": app_version}
        running_job = dm.invoke(build_params=params, securitytoken=None)

        def gen():
            yield sse((MessageTuple(key="message", value="queued"),
                       MessageTuple(key="data", value={"status": "OK"})))
            running_job.block_until_building()
            yield sse((MessageTuple(key="message", value="building"),
                       MessageTuple(key="data", value={"status": "OK"})))
            running_job.block_until_complete()
            yield sse((MessageTuple(key="message", value="success" if running_job.get_build().is_good() else "failed"),
                       MessageTuple(key="data", value={"status": "OK"})))

        return Response(gen(), content_type="text/event-stream")


if __name__ == '__main__':
    app.run(debug=True, port=int(os.getenv("PORT", "5000")))
