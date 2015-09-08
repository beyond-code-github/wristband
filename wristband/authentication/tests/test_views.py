from django.shortcuts import resolve_url
import mock

from wristband.authentication.views import login_view, logout_view

def test_login_view(rf, dummy_user_class):
    pass

def test_logout_view_wrong_method(client):
    url = resolve_url('logout')
    client.post(url)


@mock.patch('wristband.authentication.views.logout')
def test_logout_view(mocked_logout, rf):
    request = rf.get()

