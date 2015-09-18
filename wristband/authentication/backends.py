import logging

from django.contrib.auth.hashers import make_password
from django.conf import settings
from mongoengine import DoesNotExist
from mongoengine.django.mongo_auth.models import get_user_document
import ldap

logger = logging.getLogger('wristband.authentication')

class SimpleMongoLDAPBackend(object):
    """
    https://docs.djangoproject.com/en/1.4/topics/auth/#authentication-backends
    """
    user_document = get_user_document()

    LDAP_TIMEOUT = 10

    def get_user(self, user_id):
        try:
            return self.user_document.objects.get(username=user_id)
        except DoesNotExist:
            return None

    def get_or_create_user(self, username):
        kwargs = {
            'username': username,
            'defaults': {'username': username.lower(),
                         'password': make_password(None)}
        }
        return self.user_document.objects.get_or_create(**kwargs)

    def authenticate(self, username=None, password=None):
        user = None
        user_dn = settings.AUTH_LDAP_USER_DN_TEMPLATE.format(user=username)
        formatted_dn = ldap.dn.str2dn(user_dn, ldap.DN_FORMAT_LDAPV2)
        ldap_uri = settings.AUTH_LDAP_SERVER_URI
        ldap.set_option(ldap.OPT_NETWORK_TIMEOUT, self.LDAP_TIMEOUT)
        # Required when using self-signed certs
        ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
        ldap.set_option(ldap.OPT_DEBUG_LEVEL, 255)
        ldap_client = ldap.initialize(ldap_uri)
        try:
            ldap_client.simple_bind_s(formatted_dn, password)
            user, created = self.get_or_create_user(username)
            logger.info('User {username} successfully logged in'.format(username=username))
        except ldap.INVALID_CREDENTIALS:
            logger.info('User {username} not logged in, invalid credentials'.format(username=username))
        except ldap.LDAPError, e:
            # logs any other ldap error as error
            logger.error(e)
        finally:
            ldap_client.unbind()
        return user
