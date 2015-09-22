import mock
import pytest
from jenkins import JenkinsException

from wristband.providers.exceptions import DeployException
from wristband.providers.service_providers import JenkinsServiceProvider


@mock.patch('wristband.providers.service_providers.jenkins')
@mock.patch('wristband.providers.service_providers.Job')
@mock.patch('wristband.providers.service_providers.App')
@mock.patch.object(JenkinsServiceProvider, 'get_jenkins_server_config')
def test_jenkins_provider_save_job_info_successful_case(mocked_get_jenkins_server_config,
                                                        mocked_app_model,
                                                        mocked_job_model,
                                                        mocked_jenkins):
    provider_under_test = JenkinsServiceProvider('foo', 'bar')
    mocked_get_jenkins_server_config.return_value = {'username': 'john',
                                                     'password': 'password',
                                                     'uri': 'http://test.com'}

    # it's easier to monkey patch the mocked jenkins server instance here
    mocked_jenkins_server = mock.Mock()
    mocked_jenkins_server.get_job_info.return_value = {'nextBuildNumber': 5}
    mocked_jenkins_server.get_build_info.return_value = {
        'actions': [
            {
                'parameters': [
                    {'name': 'APP_BUILD_NUMBER', 'value': '0.1.0'}
                ]
            }
        ]
    }
    provider_under_test.server = mocked_jenkins_server
    provider_under_test.save_job_info('0.1.0')
    calls = [mock.call().save(),
             mock.call().id.__str__()]
    mocked_job_model.has_calls(calls, any_order=True)


@mock.patch('wristband.providers.service_providers.jenkins')
@mock.patch('wristband.providers.service_providers.Job')
@mock.patch('wristband.providers.service_providers.App')
@mock.patch.object(JenkinsServiceProvider, 'get_jenkins_server_config')
def test_jenkins_provider_save_job_info_failure_case(mocked_get_jenkins_server_config,
                                                     mocked_app_model,
                                                     mocked_job_model,
                                                     mocked_jenkins):
    provider_under_test = JenkinsServiceProvider('foo', 'bar')
    mocked_get_jenkins_server_config.return_value = {'username': 'john',
                                                     'password': 'password',
                                                     'uri': 'http://test.com'}

    # it's easier to monkey patch the mocked jenkins server instance here
    mocked_jenkins_server = mock.Mock()
    mocked_jenkins_server.get_job_info.return_value = {'nextBuildNumber': 5}
    mocked_jenkins_server.get_build_info.return_value = {
        'actions': [
            {
                'parameters': [
                    {'name': 'APP_BUILD_NUMBER', 'value': '0.1.0'}
                ]
            }
        ]
    }
    provider_under_test.server = mocked_jenkins_server
    job_id = provider_under_test.save_job_info('0.2.0')
    assert job_id is None


@mock.patch('wristband.providers.service_providers.jenkins')
@mock.patch('wristband.providers.service_providers.Job')
@mock.patch('wristband.providers.service_providers.App')
@mock.patch.object(JenkinsServiceProvider, 'get_jenkins_server_config')
def test_jenkins_provider_status_not_building_case(mocked_get_jenkins_server_config,
                                                   mocked_app_model,
                                                   mocked_job_model,
                                                   mocked_jenkins):
    provider_under_test = JenkinsServiceProvider('foo', 'bar')
    mocked_get_jenkins_server_config.return_value = {'username': 'john',
                                                     'password': 'password',
                                                     'uri': 'http://test.com'}

    # it's easier to monkey patch the mocked jenkins server instance here
    mocked_jenkins_server = mock.Mock()
    mocked_jenkins_server.get_build_info.return_value = {
        'building': False,
        'result': 'success'
    }
    provider_under_test.server = mocked_jenkins_server
    assert provider_under_test.status(job=mock.Mock()) == 'success'


@mock.patch('wristband.providers.service_providers.jenkins')
@mock.patch('wristband.providers.service_providers.Job')
@mock.patch('wristband.providers.service_providers.App')
@mock.patch.object(JenkinsServiceProvider, 'get_jenkins_server_config')
def test_jenkins_provider_status_building_case(mocked_get_jenkins_server_config,
                                               mocked_app_model,
                                               mocked_job_model,
                                               mocked_jenkins):
    provider_under_test = JenkinsServiceProvider('foo', 'bar')
    mocked_get_jenkins_server_config.return_value = {'username': 'john',
                                                     'password': 'password',
                                                     'uri': 'http://test.com'}

    # it's easier to monkey patch the mocked jenkins server instance here
    mocked_jenkins_server = mock.Mock()
    mocked_jenkins_server.get_build_info.return_value = {
        'building': 'building'
    }
    provider_under_test.server = mocked_jenkins_server
    assert provider_under_test.status(job=mock.Mock()) == 'building'


@mock.patch('wristband.providers.service_providers.jenkins.Jenkins')
@mock.patch('wristband.providers.service_providers.Job')
@mock.patch('wristband.providers.service_providers.App')
@mock.patch.object(JenkinsServiceProvider, 'get_jenkins_server_config')
def test_deploy_JenkinsException(mocked_get_jenkins_server_config,
                                 mocked_app_model,
                                 mocked_job_model,
                                 mocked_jenkins):
    provider_under_test = JenkinsServiceProvider('foo', 'bar')
    mocked_get_jenkins_server_config.return_value = {'username': 'john',
                                                     'password': 'password',
                                                     'uri': 'http://test.com'}

    mocked_jenkins.return_value.build_job.side_effect = JenkinsException('test_message')

    with pytest.raises(DeployException):
        provider_under_test.deploy(123)


@mock.patch('wristband.providers.service_providers.jenkins.Jenkins')
@mock.patch('wristband.providers.service_providers.Job')
@mock.patch('wristband.providers.service_providers.App')
@mock.patch.object(JenkinsServiceProvider, 'get_jenkins_server_config')
@mock.patch.object(JenkinsServiceProvider, 'save_job_info')
def test_deploy_success(mocked_save_job_info,
                        mocked_get_jenkins_server_config,
                        mocked_app_model,
                        mocked_job_model,
                        mocked_jenkins):
    provider_under_test = JenkinsServiceProvider('foo', 'bar')
    mocked_get_jenkins_server_config.return_value = {'username': 'john',
                                                     'password': 'password',
                                                     'uri': 'http://test.com'}

    provider_under_test.deploy(123)
    mocked_save_job_info.assert_called_once_with(123)
