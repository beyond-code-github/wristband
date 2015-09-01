import mock

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
    assert mocked_job_model.save.called_once()


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
