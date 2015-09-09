from django.http import HttpResponseNotAllowed, JsonResponse
from django.shortcuts import resolve_url
import mock
from wristband.authentication.views import login_view, logout_view


@mock.patch('wristband.authentication.views.login')
@mock.patch('wristband.authentication.views.authenticate')
def test_login_view(mocked_authenticate, mocked_login, client, django_user_model):
    mock_user = django_user_model(username='test_user')
    mocked_authenticate.return_value = mock_user

    url = resolve_url('login')
    response = client.post(url, {'username': 'test_user', 'password': 'password'})
    mocked_authenticate.assert_called_with(username='test_user', password='password')
    assert isinstance(response, JsonResponse)
    assert response.status_code == 200
    assert 'session_key' in response.content


@mock.patch('wristband.authentication.views.authenticate')
def test_login_view_bad_credential(mocked_authenticate, rf):
    mocked_authenticate.return_value = None

    url = resolve_url('login')
    request = rf.post(url, {'username': 'test_user', 'password': 'password'})
    response = login_view(request)
    mocked_authenticate.assert_called_with(username='test_user', password='password')
    assert 'message' in response.content
    assert isinstance(response, JsonResponse)
    assert response.status_code == 403


def test_login_view_wrong_method(client):
    url = resolve_url('login')
    response = client.get(url)
    assert isinstance(response, HttpResponseNotAllowed)


@mock.patch('wristband.authentication.views.logout')
def test_logout_view(mocked_logout, rf):
    url = resolve_url('logout')
    request = rf.get(url)
    response = logout_view(request)
    assert isinstance(response, JsonResponse)
    mocked_logout.assert_called_with(request)


def test_logout_view_wrong_method(client):
    url = resolve_url('logout')
    response = client.post(url)
    assert isinstance(response, HttpResponseNotAllowed)

