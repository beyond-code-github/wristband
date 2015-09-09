# https://github.com/MongoEngine/mongoengine/issues/966

from django.contrib.auth import user_logged_in
from django.middleware.csrf import rotate_token
from bson.objectid import ObjectId

SESSION_KEY = '_auth_user_id'
BACKEND_SESSION_KEY = '_auth_user_backend'
HASH_SESSION_KEY = '_auth_user_hash'


def get_user_session_key(request):
    # This value in the session is always serialized to a string, so we need
    # to convert it back to Python whenever we access it.
    if SESSION_KEY in request.session:
        return ObjectId(request.session[SESSION_KEY])


def login(request, user):
    """
    Persist a user id and a backend in the request. This way a user doesn't
    have to reauthenticate on every request. Note that data set during
    the anonymous session is retained when the user logs in.


    This a copy of the django implementation, it's just using str(user.pk) instead of
    user._meta.pk becase the Mongo models don't have _meta as a class instance
    """
    session_auth_hash = ''
    if user is None:
        user = request.user
    if hasattr(user, 'get_session_auth_hash'):
        session_auth_hash = user.get_session_auth_hash()

    if SESSION_KEY in request.session:
        if get_user_session_key(request) != user.pk or (
                    session_auth_hash and
                        request.session.get(HASH_SESSION_KEY) != session_auth_hash):
            # To avoid reusing another user's session, create a new, empty
            # session if the existing session corresponds to a different
            # authenticated user.
            request.session.flush()
    else:
        request.session.cycle_key()
    request.session[SESSION_KEY] = str(user.pk)
    request.session[BACKEND_SESSION_KEY] = user.backend
    request.session[HASH_SESSION_KEY] = session_auth_hash
    if hasattr(request, 'user'):
        request.user = user
    rotate_token(request)
    user_logged_in.send(sender=user.__class__, request=request, user=user)
