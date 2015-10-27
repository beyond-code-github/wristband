# -*- coding: utf-8 -*-
'''
Test settings

'''

from .common import *  # noqa

# DEBUG
# ------------------------------------------------------------------------------
DEBUG = env.bool('DJANGO_DEBUG', default=False)
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key only used for development and testing.
SECRET_KEY = env("DJANGO_SECRET_KEY", default='CHANGEME!!!')

# AUTHENTICATION
# --------------
AUTH_LDAP_SERVER_URI = ''
AUTH_LDAP_USER_DN_TEMPLATE = ''
AUTH_LDAP_BIND_AS_AUTHENTICATING_USER = False

AUTHENTICATION_BACKENDS = (
    'wristband.test_utils.backends.DummyBackend',
)


WRISTBAND_ENV = 'test'
ADMIN_LOGIN = 'admin'
ADMIN_PASSWORD = 'pbkdf2_sha256$20000$L2eoHXHWJuFY$N4WSNDaL4YUp7/Ghw7jgFL30aHdToLgI6REfKVBn/ps='

