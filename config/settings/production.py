# -*- coding: utf-8 -*-
'''
Production Configurations

- Use djangosecure

'''
from __future__ import absolute_import, unicode_literals

import ldap
from django_auth_ldap.config import LDAPSearch, GroupOfNamesType

from .common import *  # noqa



# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Raises ImproperlyConfigured exception if DJANGO_SECRET_KEY not in os.environ
SECRET_KEY = env("DJANGO_SECRET_KEY")


# django-secure
# ------------------------------------------------------------------------------
INSTALLED_APPS += ("djangosecure",)

SECURITY_MIDDLEWARE = (
    'djangosecure.middleware.SecurityMiddleware',
)

# Make sure djangosecure.middleware.SecurityMiddleware is listed first
MIDDLEWARE_CLASSES = SECURITY_MIDDLEWARE + MIDDLEWARE_CLASSES

# set this to 60 seconds and then to 518400 when you can prove it works
SECURE_HSTS_SECONDS = 60
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool("DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True)
SECURE_FRAME_DENY = env.bool("DJANGO_SECURE_FRAME_DENY", default=True)
SECURE_CONTENT_TYPE_NOSNIFF = env.bool("DJANGO_SECURE_CONTENT_TYPE_NOSNIFF", default=True)
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_HTTPONLY = True

# SITE CONFIGURATION
# ------------------------------------------------------------------------------
# Hosts/domain names that are valid for this site
# See https://docs.djangoproject.com/en/1.6/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["*"]
# END SITE CONFIGURATION


INSTALLED_APPS += ("gunicorn",)

# AUTHENTICATION
# --------------
AUTH_LDAP_SERVER_URI = env('AUTH_LDAP_SERVER_URI')
AUTH_LDAP_BIND_AS_AUTHENTICATING_USER = env('AUTH_LDAP_BIND_AS_AUTHENTICATING_USER', default=True)

AUTH_LDAP_GLOBAL_OPTIONS = {
    ldap.OPT_X_TLS_REQUIRE_CERT: ldap.OPT_X_TLS_NEVER,
    ldap.OPT_NETWORK_TIMEOUT: 10,
    ldap.OPT_DEBUG_LEVEL: 255
}

AUTH_LDAP_BIND_DN = ''
AUTH_LDAP_BIND_PASSWORD = ''
AUTH_LDAP_USER_SEARCH_DN = env('AUTH_LDAP_USER_SEARCH_DN')
AUTH_LDAP_GROUP_SEARCH_DN = env('AUTH_LDAP_GROUP_SEARCH_DN')
AUTH_LDAP_SUPERUSER_DN = env('AUTH_LDAP_SUPERUSER_DN')

AUTH_LDAP_USER_SEARCH = LDAPSearch(AUTH_LDAP_USER_SEARCH_DN, ldap.SCOPE_SUBTREE, "(uid=%(user)s)")
AUTH_LDAP_GROUP_SEARCH = LDAPSearch(AUTH_LDAP_GROUP_SEARCH_DN, ldap.SCOPE_SUBTREE, "(objectClass=groupOfNames)")
AUTH_LDAP_GROUP_TYPE = GroupOfNamesType()
AUTH_LDAP_CACHE_GROUPS = True
AUTH_LDAP_GROUP_CACHE_TIMEOUT = 300
AUTH_LDAP_USER_FLAGS_BY_GROUP = {
    "is_superuser": AUTH_LDAP_SUPERUSER_DN
}
