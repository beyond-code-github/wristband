from collections import namedtuple
from urlparse import urlparse
import logging

from flask import Blueprint, Response, current_app, session
from flask.ext.restful import reqparse
from flask_restful import Api, Resource
from jenkinsapi.jenkins import Jenkins

from utils import get_all_releases, get_all_app_names, get_all_releases_of_app_in_env, \
    get_all_pipelines, get_all_environments, make_environment_groups, sse, extract_environment_parts, \
    get_jenkins_uri, log_formatter
from auth import AuthenticatedResource, ldap_authentication

MessageTuple = namedtuple('MessageTuple', ['key', 'value'])

API_VERSION_V1 = 1
API_VERSION = API_VERSION_V1

api_v1_bp = Blueprint('api_v1', __name__)
api_v1 = Api(api_v1_bp)

parser = reqparse.RequestParser()
parser.add_argument('username', type=str)
parser.add_argument('password', type=str)

@api_v1.resource('/login')
class Login(Resource):
    """
    Ty to authenticate against LDAP, if successful drop a cookie to remember the user session
    """

    def post(self):
        args = parser.parse_args()
        username = args['username']
        password = args['password']
        user = ldap_authentication(username, password)
        if user:
            session['authenticated'] = True
            session['username'] = username
            return {'status': 'Authorised'}
        else:
            return {'status': 'Unauthorised'}, 401


@api_v1.resource('/logout')
class Logout(AuthenticatedResource):
    def get(self):
        try:
            del session['authenticated']
            del session['username']
        except KeyError:
            # keys are not there for whaterver reason, do nothing
            pass
        return {'status': 'OK'}


@api_v1.resource('/config')
class Config(AuthenticatedResource):
    def get(self):
        pipelines = get_all_pipelines()
        all_releases = get_all_releases()
        environments = get_all_environments()
        envgroups = make_environment_groups(environments)
        response = {'pipelines': pipelines, 'envs': envgroups, "apps": []}

        # change this into the releases app
        for app in get_all_app_names(all_releases):
            response['apps'].append({'name': app, 'envs': {}})
            for env in environments:
                versions = get_all_releases_of_app_in_env(env, app, all_releases)
                if versions:
                    response['apps'][-1]['envs'][env] = {'versions': versions}
        return response


@api_v1.resource('/promote/<deploy_env>/<app_name>/<app_version>')
class Promotion(AuthenticatedResource):
    def get(self, deploy_env, app_name, app_version):
        deploy_env = extract_environment_parts(deploy_env)
        pipeline = get_all_pipelines()[deploy_env.security_level]
        environment_index = pipeline.index(deploy_env.full_name)
        previous_environment_index = environment_index - 1

        if environment_index != 0:
            # We're not the first environment in the pipeline, check previous
            releases = get_all_releases()
            # this should come from the releases app
            environments_with_same_app_version = map(lambda r: r['environment'],
                                                     filter(lambda r: r['app_name'] == app_name and r['version'] == app_version,
                                                            releases))
            previous_environment = pipeline[previous_environment_index]
            if previous_environment not in environments_with_same_app_version:
                return {"error": "you need to deploy {} to {} first".format(app_version, previous_environment)}, 400

        jenkins_uri = get_jenkins_uri(current_app.config['ENVIRONMENTS'], deploy_env.full_name)
        if jenkins_uri:
            parsed_jenkins_uri = urlparse(jenkins_uri)
            jenkins = Jenkins(
                jenkins_uri.replace(
                    "{username}:{password}@".format(username=parsed_jenkins_uri.username,
                                                    password=parsed_jenkins_uri.password),
                    ""),
                username=parsed_jenkins_uri.username, password=parsed_jenkins_uri.password)

            dm = jenkins.get_job("deploy-microservice")
            params = {"APP": app_name, "APP_BUILD_NUMBER": app_version}
            running_job = dm.invoke(build_params=params, securitytoken=None)
            username = session['username']
            logging.info(log_formatter(
                '{user} promoted {app}-{version} to {env}'.format(user=username,
                                                                  app=app_name,
                                                                  version=app_version,
                                                                  env=deploy_env.full_name)
            ))

            def gen():
                yield sse('queued', {'status': 'OK'})
                running_job.block_until_building()
                yield sse('building', {'status': 'OK'})
                running_job.block_until_complete()
                yield sse('success' if running_job.get_build().is_good() else 'failed', {'status': 'OK'})

            return Response(gen(), content_type="text/event-stream")
        else:
            return {'error': '{environment} does not exist'.format(environment=deploy_env.full_name)}
