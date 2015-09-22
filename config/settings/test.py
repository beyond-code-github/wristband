# -*- coding: utf-8 -*-
'''
Test settings

'''

from .common import *  # noqa

# DEBUG
# ------------------------------------------------------------------------------
DEBUG = env.bool('DJANGO_DEBUG', default=False)
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG
TEST_ENV = True

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

REST_FRAMEWORK = {} # disable any auth/permission not defined at the class level