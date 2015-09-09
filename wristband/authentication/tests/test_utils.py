from django.contrib.sessions.backends.base import SessionBase
import mock
from wristband.authentication.utils import get_user_session_key, login

MOCK_SESSION_KEY = 'test_key'

@mock.patch('wristband.authentication.utils.SESSION_KEY', MOCK_SESSION_KEY)
@mock.patch('wristband.authentication.utils.ObjectId')
def test_get_user_session_key(mock_object_id):
    """
    Check this uses ObjectId
    """

    session = {MOCK_SESSION_KEY: 'user_pk'}
    mock_request = mock.Mock(session=session)
    get_user_session_key(request=mock_request)
    mock_object_id.assert_called_with('user_pk')


class DummySession(SessionBase):
    def cycle_key(self):
        pass


@mock.patch('wristband.authentication.utils.SESSION_KEY', MOCK_SESSION_KEY)
@mock.patch('wristband.authentication.utils.rotate_token', mock.MagicMock())
@mock.patch('wristband.authentication.utils.ObjectId')
@mock.patch('wristband.authentication.utils.user_logged_in', mock.MagicMock())
def test_login(mock_object_id, dummy_user_class):
    """
    Only checks that the session key value is the user pk and it's a string
    The rest is Django code
    """
    mock_object_id.return_value = 1
    user = dummy_user_class(username='test_user', pk=1)
    user.backend = 'test_backend'
    session = DummySession()
    session[MOCK_SESSION_KEY] = 'user_pk'
    mock_request = mock.Mock(session=session)
    login(mock_request, user)
    assert session[MOCK_SESSION_KEY] == '1'
    assert isinstance(session[MOCK_SESSION_KEY], str)
