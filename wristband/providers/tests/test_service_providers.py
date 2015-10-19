import mock
import pytest
import requests

from wristband.apps.models import App
from wristband.providers.exceptions import DeployException
from wristband.providers.service_providers import DocktorServiceProvider


@mock.patch.object(DocktorServiceProvider, 'get_docktor_server_config')
@mock.patch('wristband.providers.service_providers.requests')
def test_docktor_provider_deploy_success(mocked_requests, mocked_get_docktor_server_config, settings):
    settings.WEBSTORE_URL = 'https://webstore.com'
    app = App(name='foo', stage='bar')
    app.save()
    mocked_get_docktor_server_config.return_value = {'username': 'john',
                                                     'password': 'password',
                                                     'uri': 'http://test.com'}
    provider_under_test = DocktorServiceProvider('foo')

    provider_under_test.deploy('0.1.0')
    calls = [mock.call().patch('http://test.com/apps/foo',
                               data={'slug_uri': 'https://webstore.com/apps/foo/foo_0.1.0.tgz'}),
             mock.call().patch().raise_for_status()]
    mocked_requests.has_calls(calls)


@mock.patch.object(DocktorServiceProvider, 'get_docktor_server_config')
@mock.patch('wristband.providers.service_providers.requests')
def test_deploy_failed(mocked_requests, mocked_get_docktor_server_config):
    app = App(name='foo', stage='bar')
    app.save()
    mocked_get_docktor_server_config.return_value = {'username': 'john',
                                                     'password': 'password',
                                                     'uri': 'http://test.com'}
    mocked_requests.patch.return_value.raise_for_status.side_effect = requests.HTTPError('test_message')
    provider_under_test = DocktorServiceProvider('foo')

    with pytest.raises(DeployException):
        provider_under_test.deploy(123)
