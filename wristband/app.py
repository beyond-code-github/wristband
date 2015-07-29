import types
from urlparse import urlparse
from collections import namedtuple
import os

from flask import Response
from flask_restful import Resource
from jenkinsapi.jenkins import Jenkins
from flask import Flask
from flask.ext.restful import Api

from utils import get_all_releases, get_all_app_names, get_all_releases_of_app_in_env, \
    get_all_pipelines, get_all_environments, make_environment_groups, sse

app = Flask(__name__)
app.config.from_envvar("CONFIG_FILE", "config/production.py")
api = Api(app)

MessageTuple = namedtuple('MessageTuple', ['key', 'value'])


def api_route(self, *args, **kwargs):
    def wrapper(cls):
        self.add_resource(cls, *args, **kwargs)
        return cls

    return wrapper


api.route = types.MethodType(api_route, api)


@api.route('/ping')
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
            yield sse((MessageTuple(key="event", value="queued"),
                       MessageTuple(key="data", value={"status": "OK"})))
            running_job.block_until_building()
            yield sse((MessageTuple(key="event", value="building"),
                       MessageTuple(key="data", value={"status": "OK"})))
            running_job.block_until_complete()
            yield sse((MessageTuple(key="event", value="success" if running_job.get_build().is_good() else "failed"),
                       MessageTuple(key="data", value={"status": "OK"})))

        return Response(gen(), content_type="text/event-stream")


if __name__ == '__main__':
    app.run(debug=True, port=int(os.getenv("PORT", "5000")))
