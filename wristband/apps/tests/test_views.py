import mock

from wristband.providers.generics import DeployException


@mock.patch('wristband.apps.views.JenkinsServiceProvider')
def test_patched_deploy_exception(mocked_jenkins_service_provider, client):
    mocked_jenkins_service_provider.return_value.deploy.side_effect = DeployException('test_message')
    response = client.put('/api/apps/coronationstreet/stages/qa/version/1.0.1/')
    assert response.content == '{"detail":"test_message"}'
    assert response.status_code == 500

@mock.patch('wristband.apps.views.JenkinsServiceProvider')
def test_patched_deploy_success(mocked_jenkins_service_provider, client):
    mocked_jenkins_service_provider.return_value.deploy.return_value = 2354
    response = client.put('/api/apps/coronationstreet/stages/qa/version/1.0.1/')
    assert response.content == '{"job_id":2354}'
    assert response.status_code == 200