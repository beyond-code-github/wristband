from functools import wraps
import json
import re
from collections import namedtuple
from itertools import chain

from flask import current_app
import requests

MAPPING_KEYS = {
    'an': 'app_name',
    'env': 'environment',
    'fs': 'first_seen',
    'ls': 'last_seen',
    'ver': 'version'
}
ENVIRONMENT_REGEX = r'^((?P<env>\w+)-(?P<security_level>\w+))$'
RELEASES_APP_ENDPOINT = "https://releases.tax.service.gov.uk/{endpoint}"

EnvironmentsParts = namedtuple('EnvironmentParts', ['full_name', 'env', 'security_level'])


def humanise_release_dict(release_dict):
    new_dict = {}
    for k, v in release_dict.iteritems():
        if k in MAPPING_KEYS:
            new_dict[MAPPING_KEYS[k]] = v
    return new_dict


def extract_environment_parts(environment_name):
    m = re.search(ENVIRONMENT_REGEX, environment_name)
    env = m.group('env') if m else None
    security_level = m.group('security_level') if m else None

    return EnvironmentsParts(full_name=environment_name,
                             env=env,
                             security_level=security_level)


def get_all_releases():
    url = RELEASES_APP_ENDPOINT.format(endpoint='apps')
    response = requests.get(url)
    if response:
        releases = [humanise_release_dict(release) for release in response.json()]
    else:
        releases = []
    return releases


def remove_unwanted_keys_from_dict(dictionary, allowed_keys=None):
    allowed_keys = allowed_keys or ('version', 'last_seen')
    return {key: dictionary[key] for key in dictionary if key in allowed_keys}


def get_all_releases_of_app_in_env(deploy_env, app_name, releases):
    # This feels a bit nasty and convoluted, it should come from the releases app
    releases_for_env = filter(lambda r: r['environment'] == deploy_env and r['app_name'] == app_name, releases)
    sorted_releases_for_env = sorted(releases_for_env, key=lambda r: r['last_seen'], reverse=True)
    return map(remove_unwanted_keys_from_dict, sorted_releases_for_env)


def get_all_app_names(releases):
    return frozenset([release['app_name'] for release in releases])


def get_all_pipelines():
    return current_app.config.get('PIPELINES')


def get_all_environments():
    return sorted(chain.from_iterable(map(get_envs_in_pipeline, get_all_pipelines())))


def get_envs_in_pipeline(pipeline):
    try:
        return get_all_pipelines()[pipeline]
    except KeyError:
        return []


def make_environment_groups(environments):
    shortenvs = frozenset([extract_environment_parts(environment).env for environment in environments])
    envgroups = {}
    for shortenv in shortenvs:
        envgroups[shortenv] = [env for env in environments if shortenv in env]
    return envgroups


def sse(event, data):
    return "".join([
        "event: {}\n".format(event),
        "data: {}\n\n".format(json.dumps(data))
    ])


def get_jenkins_uri(environments, deploy_env_name):
    try:
        return environments[deploy_env_name]["jenkins_uri"]
    except KeyError:
        return None


def log_formatter(message):
    return json.dumps({'app': 'wristband-frontend', 'message': message})
