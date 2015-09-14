import mock
from ldap import INVALID_CREDENTIALS, LDAPError
import pytest

from wristband.authentication.backends import SimpleMongoLDAPBackend


@mock.patch('wristband.authentication.backends.ldap')
def test_ldap_failed_authentication(mocked_ldap):
    mocked_ldap.initialize.return_value.simple_bind_s.side_effect = INVALID_CREDENTIALS
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


@mock.patch('wristband.authentication.backends.logger')
@mock.patch('wristband.authentication.backends.ldap')
def test_logging_ldap_failed_authentication(mocked_ldap, mocked_logger):
    mocked_ldap.initialize.return_value.simple_bind_s.side_effect = INVALID_CREDENTIALS
    backend = SimpleMongoLDAPBackend()
    with pytest.raises(INVALID_CREDENTIALS):
        backend.authenticate('test_user', 'password')
        mocked_logger.info.assert_called_with('User user_test not logged in, invalid credentials')


@mock.patch('wristband.authentication.backends.logger')
@mock.patch.object(SimpleMongoLDAPBackend, 'get_or_create_user')
@mock.patch('wristband.authentication.backends.ldap')
def test_logging_ldap_successful_authentication(mocked_ldap, mock_get_or_create_user, mocked_logger, dummy_user_class):
    dummy_user = dummy_user_class(username='test_user')
    mock_get_or_create_user.return_value = dummy_user, False
    mocked_simple_bind_s = mock.Mock(return_value=True)
    mocked_ldap.initialize.return_value = mock.Mock(simple_bind_s=mocked_simple_bind_s)
    backend = SimpleMongoLDAPBackend()
    backend.authenticate('test_user', 'password')
    mocked_logger.info.assert_called_with('User test_user successfully logged in')


@mock.patch('wristband.authentication.backends.logger')
@mock.patch('wristband.authentication.backends.ldap')
def test_logging_ldap_server_error(mocked_ldap, mocked_logger):
    mocked_ldap.initialize.return_value.simple_bind_s.side_effect = LDAPError('test_error_message')
    backend = SimpleMongoLDAPBackend()
    with pytest.raises(LDAPError):
        backend.authenticate('test_user', 'password')
        mocked_logger.info.assert_called_with('test_error_message')
