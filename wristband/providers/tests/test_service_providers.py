from wristband.providers.service_providers import JenkinsServiceProvider

@mock.patch('wristband.providers.service_providers.jenkins')
def test_jenkins_provider_save_job_info(mocked_jenkins):
    mocked_jenkins.get_job_info.return_value = {'nextBuildNumber': 5}
    mocked_jenkins.get_build_info.return_value = {
        'actions': [
            {
                'paramenters': [
                    {'name': 'APP_BUILD_NUMBER', 'value': '0.1.0'}
                ]
            }
        ]
    }
