from functools import wraps

from flask.ext.restful import Resource, abort
from flask import session, current_app
import ldap


def ldap_authentication(username, password):
    authenticated = False
    ldap_conf = current_app.config['LDAP']
    user_dn = ldap_conf['user_dn'].format(username=username)
    ldap_client = ldap.initialize(ldap_conf['url'])
    try:
        ldap_client.simple_bind_s(user_dn, password)
        authenticated = True
    except ldap.INVALID_CREDENTIALS:
        pass
    finally:
        ldap_client.unbind()
        return authenticated


def authenticate(func):
    """
    Implement a rudimentary remember me functionality by checking if a key is stored in the secure cookie
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_app.authentication_enabled:
            # not in testing mode, check auth
            if not getattr(func, 'authenticate', True):
                return func(*args, **kwargs)
            if session.get('authenticated', False):
                return func(*args, **kwargs)
            abort(401)
        else:
            # skip authentication for testing purposes
            return func(*args, **kwargs)

    return wrapper


class AuthenticatedResource(Resource):
    method_decorators = [authenticate]
