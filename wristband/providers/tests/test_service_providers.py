import mock
import pytest
from jenkins import JenkinsException

from wristband.providers.exceptions import DeployException
from wristband.providers.service_providers import DocktorServiceProvider


@mock.patch.object(DocktorServiceProvider, 'get_docktor_server_config')
def test_docktor_provider_deploy_success(mocked_get_docktor_server_config):
    provider_under_test = DocktorServiceProvider('foo', 'bar')
    mocked_get_docktor_server_config.return_value = {'username': 'john',
                                                     'password': 'password',
                                                     'uri': 'http://test.com'}

    # it's easier to monkey patch the mocked jenkins server instance here
    mocked_server = mock.Mock()
    provider_under_test.server = mocked_server
    provider_under_test.deploy('0.1.0')
    mocked_server.patch.assert_called()



@mock.patch('wristband.providers.service_providers.jenkins.Jenkins')
@mock.patch('wristband.providers.service_providers.Job')
@mock.patch('wristband.providers.service_providers.App')
@mock.patch.object(DocktorServiceProvider, 'get_jenkins_server_config')
def test_deploy_JenkinsException(mocked_get_jenkins_server_config,
                                 mocked_app_model,
                                 mocked_job_model,
                                 mocked_jenkins):
    provider_under_test = DocktorServiceProvider('foo', 'bar')
    mocked_get_jenkins_server_config.return_value = {'username': 'john',
                                                     'password': 'password',
                                                     'uri': 'http://test.com'}

    mocked_jenkins.return_value.build_job.side_effect = JenkinsException('test_message')

    with pytest.raises(DeployException):
        provider_under_test.deploy(123)
