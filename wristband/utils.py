import re
from collections import namedtuple
from itertools import chain

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


def get_all_releases_of_app_in_env(deploy_env, app_name, releases):
    releases_for_env = filter(lambda r: r['environment'] == deploy_env and r['app_name'] == app_name, releases)
    return sorted(releases_for_env, key=lambda r: r['last_seen'], reverse=True)


def get_all_app_names(releases):
    return frozenset([release['app_name'] for release in releases])


def get_all_app_names_in_env(env, releases):
    return frozenset(filter(lambda r: r['environment'] == env, releases))


def get_all_pipelines():
    # circular import, should probably fix this properly
    from app import app
    return app.config.get('PIPELINES')


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


def sse(messages):
    """
    :param messages: Tuple of named tuples contaning key and data
    :return:
    """
    return "".join(["{key}: {value}".format(key=message.key, value=str(message.value)) for message in messages])


def get_jenkins_uri(environments, deploy_env_name):
    try:
        return environments[deploy_env_name]["jenkins_uri"]
    except KeyError:
        return None
