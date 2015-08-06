import json

import mock
import pytest
from flask import url_for


def test_ping(client):
    url = url_for('main_app.ping')
    resource = client.get(url)
    assert json.loads(resource.data) == {'status': 'OK'}


@mock.patch('app.ldap_authentication')
@mock.patch('app.session', new_callable=dict)
def test_login_successful(mocked_session, mocked_ldap_authentication, client):
    """
    For what we care in this test the session behaves like a dictionary
    Session is then replaced with a dictionary for easy testing
    """
    mocked_ldap_authentication.return_value = True
    url = url_for('main_app.login')
    resource = client.post(url, data={'username': 'username', 'password': 'password'})
    assert json.loads(resource.data) == {'status': 'Authorised'}
    assert resource.status_code == 200
    assert mocked_session['authenticated'] is True
    assert mocked_session['username'] == 'username'


@mock.patch('app.ldap_authentication')
@mock.patch('app.session', new_callable=dict)
def test_login_failed(mocked_session, mocked_ldap_authentication, client):
    """
    For what we care in this test the session behaves like a dictionary
    Session is then replaced with a dictionary for easy testing
    """
    mocked_ldap_authentication.return_value = False
    url = url_for('main_app.login')
    resource = client.post(url, data={'username': 'username', 'password': 'password'})
    assert json.loads(resource.data) == {'status': 'Unauthorised'}
    assert resource.status_code == 401
    assert 'authenticated' not in mocked_session
    assert 'username' not in mocked_session


@pytest.mark.parametrize(('mocked_session', ), [
    (
        {'authenticated': True, 'username': 'test_username'},
    ),
    (
        {},
    )
])
def test_logout(mocked_session, client):
    with mock.patch('app.session', new_callable=dict) as ms:
        ms.update(mocked_session)
        url = url_for('main_app.logout')
        resource = client.get(url)
        assert 'authenticated' not in ms
        assert 'username' not in ms
        assert json.loads(resource.data) == {'status': 'OK'}
        assert resource.status_code == 200
