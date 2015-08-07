import mock
import ldap

from auth import ldap_authentication


@mock.patch('auth.ldap')
def test_ldap__failed_authentication(mocked_ldap, client):
    mocked_simple_bind_s = mock.Mock(side_effect=ldap.INVALID_CREDENTIALS)
    mocked_ldap.initialize.return_value = mock.Mock(simple_bind_s=mocked_simple_bind_s)
    assert ldap_authentication('test', 'password') is False


@mock.patch('auth.ldap')
def test_ldap_successful_authentication(mocked_ldap, client):
    mocked_simple_bind_s = mock.Mock(return_value=True)
    mocked_ldap.initialize.return_value = mock.Mock(simple_bind_s=mocked_simple_bind_s)
    assert ldap_authentication('test', 'password') is True
