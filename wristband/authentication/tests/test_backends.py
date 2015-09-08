import mock
from ldap import INVALID_CREDENTIALS
import py

from wristband.authentication.backends import SimpleMongoLDAPBackend


@mock.patch('wristband.authentication.backends.ldap')
def test_ldap_failed_authentication(mocked_ldap):
    mocked_simple_bind_s = mock.Mock(side_effect=INVALID_CREDENTIALS)
    mocked_ldap.initialize.return_value = mock.Mock(simple_bind_s=mocked_simple_bind_s)
    backend = SimpleMongoLDAPBackend()
    with pytest.raises(INVALID_CREDENTIALS):
        assert backend.authenticate('test_user', 'password') is None
        mocked_ldap.initialize().unbind.assert_called_with()


@mock.patch.object(SimpleMongoLDAPBackend, 'get_or_create_user')
@mock.patch('wristband.authentication.backends.ldap')
def test_ldap_successful_authentication(mocked_ldap, mock_get_or_create_user, dummy_user_class):
    dummy_user = dummy_user_class(username='test_user')
    mock_get_or_create_user.return_value = dummy_user, False
    mocked_simple_bind_s = mock.Mock(return_value=True)
    mocked_ldap.initialize.return_value = mock.Mock(simple_bind_s=mocked_simple_bind_s)
    backend = SimpleMongoLDAPBackend()
    assert backend.authenticate('test_user', 'password') == dummy_user
    mocked_ldap.initialize().unbind.assert_called_with()
