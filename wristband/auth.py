from functools import wraps

from flask.ext.restful import Resource, abort
from flask import session, current_app
import ldap


def ldap_authentication(username, password):
    ldap_conf = current_app['LDAP']
    user_dn = ldap_conf['user_dn'].format(username=username)
    ldap_client = ldap.initialize(ldap['url'])
    try:
        ldap_client.simple_bind_s(user_dn, password)
        return True
    except ldap.INVALID_CREDENTIALS:
        ldap_client.unbind()
        return False


def authenticate(func):
    """
    Implement a rudimentary remember me functionality by checking if a key is stored in the secure cookie
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        if not getattr(func, 'authenticated', True):
            return func(*args, **kwargs)

        if session.get('authenticated', False):
            return func(*args, **kwargs)
        abort(401)

    return wrapper


class AuthenticatedResource(Resource):
    method_decorators = [authenticate]
