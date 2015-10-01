import mock

from wristband.providers.exceptions import DeployException


@mock.patch('wristband.apps.views.DocktorServiceProvider')
def test_patched_deploy_exception(mocked_docktor_service_provider, api_client):
    mocked_docktor_service_provider.return_value.deploy.side_effect = DeployException('test_message')
    api_client.login(username='admin', password='password')
    response = api_client.put('/api/apps/coronationstreet/stages/qa/version/1.0.1/')
    assert response.content == '{"detail":"test_message"}'
    assert response.status_code == 500


@mock.patch('wristband.apps.views.DocktorServiceProvider')
def test_patched_deploy_success(mocked_docktor_service_provider, api_client):
    mocked_docktor_service_provider.return_value.deploy.return_value = 2354
    api_client.login(username='admin', password='password')
    response = api_client.put('/api/apps/coronationstreet/stages/qa/version/1.0.1/')
    assert response.content == '{"job_id":2354}'
    assert response.status_code == 200
