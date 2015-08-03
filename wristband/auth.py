from functools import wraps
from flask.ext.restful import Resource


def ldap_authentication(username, password):
    return True


def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not getattr(func, 'authenticated', True):
            return func(*args, **kwargs)

        acct = True  # custom account lookup function

        if acct:
            return func(*args, **kwargs)

        restful.abort(401)
    return wrapper


class AuthenticatedResource(Resource):
    method_decorators = [authenticate]