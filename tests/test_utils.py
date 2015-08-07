import mock
from mock import Mock
import pytest

from utils import humanise_release_dict, extract_environment_parts, get_all_releases, EnvironmentsParts, \
    make_environment_groups, get_jenkins_uri


@pytest.mark.parametrize(('dictionary', 'expected_result'), [
    (
            {
                'an': 'test_name',
                'env': 'test_environment',
                'fs': 'test_first_seen',
                'ls': 'test_last_seen',
                'ver': 'test_version'
            },
            {
                'app_name': 'test_name',
                'environment': 'test_environment',
                'first_seen': 'test_first_seen',
                'last_seen': 'test_last_seen',
                'version': 'test_version'
            }
    ), (
            {
                'an': 'test_name',
                'env': 'test_environment',
                'fs': 'test_first_seen',
                'ls': 'test_last_seen',
                'ver': 'test_version',
                'not_converted': 'test_not_converted'
            },
            {
                'app_name': 'test_name',
                'environment': 'test_environment',
                'first_seen': 'test_first_seen',
                'last_seen': 'test_last_seen',
                'version': 'test_version'
            }
    )
])
def test_humanise_release_dict(dictionary, expected_result):
    assert humanise_release_dict(dictionary) == expected_result


@pytest.mark.parametrize(('env_name', 'expected_result'), [
    ('qa-left', EnvironmentsParts(full_name='qa-left', env='qa', security_level='left')),
    ('dev', EnvironmentsParts(full_name='dev', env=None, security_level=None))
])
def test_extract_environments_parts(env_name, expected_result):
    assert extract_environment_parts(env_name) == expected_result


@pytest.mark.parametrize(('mock_response', 'expected_result'), [
    (False, []),
    (Mock(), [{'app_name': 'test'}])
])
def test_get_all_releases(mock_response, expected_result):
    with mock.patch('utils.requests.get') as mock_get:
        if mock_response:
            mock_response.json.return_value = [{'an': 'test'}]
        mock_get.return_value = mock_response
        assert get_all_releases() == expected_result


def test_make_environment_groups():
    environments = ['qa-one', 'qa-two', 'staging-one', 'staging-two']
    assert make_environment_groups(environments) == {'qa': ['qa-one', 'qa-two'],
                                                     'staging': ['staging-one', 'staging-two']}


@pytest.mark.parametrize(('environments', 'deploy_env_name', 'expected_uri'), [
    (
            {
                'staging-left': {'jenkins_uri': 'https://user:password@url.com'},
                'qa-right': {'jenkins_uri': 'https://user:password@url.com'},
                'staging-right': {'jenkins_uri': 'https://user:password@url.com'}
            },
            'not_existing_env',
            None
    ),
    (
            {
                'staging-left': {'jenkins_uri': 'https://user:password@url.com'},
                'qa-right': {'jenkins_uri': 'https://user:password@url.com'},
                'staging-right': {'jenkins_uri': 'https://user:password@url.com'}
            },
            'qa-right',
            'https://user:password@url.com'
    )
])
def test_get_jenkins_uri(environments, deploy_env_name, expected_uri):
    assert get_jenkins_uri(environments, deploy_env_name) == expected_uri
