# -*- coding: utf-8 -*-
'''
Local settings

- Run in Debug mode
- Use console backend for emails
- Add Django Debug Toolbar
- Add django-extensions as app
'''
import ldap
from django_auth_ldap.config import LDAPSearch, GroupOfNamesType

from .common import *  # noqa


# DEBUG
# ------------------------------------------------------------------------------
DEBUG = env.bool('DJANGO_DEBUG', default=True)
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key only used for development and testing.
SECRET_KEY = env("DJANGO_SECRET_KEY", default='CHANGEME!!!')

# django-debug-toolbar
# ------------------------------------------------------------------------------
MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
INSTALLED_APPS += ('debug_toolbar', )

INTERNAL_IPS = ('127.0.0.1', '10.0.2.2',)

DEBUG_TOOLBAR_CONFIG = {
    'DISABLE_PANELS': [
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ],
    'SHOW_TEMPLATE_CONTEXT': True,
}

# django-extensions
# ------------------------------------------------------------------------------
INSTALLED_APPS += ('django_extensions', )


# AUTHENTICATION
# --------------
AUTH_LDAP_SERVER_URI = 'ldaps://localhost'
AUTH_LDAP_BIND_AS_AUTHENTICATING_USER = True


AUTH_LDAP_GLOBAL_OPTIONS = {
    ldap.OPT_X_TLS_REQUIRE_CERT: ldap.OPT_X_TLS_NEVER,
    ldap.OPT_NETWORK_TIMEOUT: 10,
    ldap.OPT_DEBUG_LEVEL: 255
}

AUTH_LDAP_BIND_DN = ''
AUTH_LDAP_BIND_PASSWORD = ''
AUTH_LDAP_USER_SEARCH = LDAPSearch("ou=users,dc=example,dc=com", ldap.SCOPE_SUBTREE, "(uid=%(user)s)")
AUTH_LDAP_USER_FLAGS_BY_GROUP = {
    "is_superuser": "cn=planets,ou=groups,dc=example,dc=com"
}
AUTH_LDAP_GROUP_SEARCH = LDAPSearch("ou=groups,dc=example,dc=com", ldap.SCOPE_SUBTREE, "(objectClass=groupOfNames)")
AUTH_LDAP_GROUP_TYPE = GroupOfNamesType()
AUTH_LDAP_CACHE_GROUPS = True
AUTH_LDAP_GROUP_CACHE_TIMEOUT = 300

