from django.contrib.auth.hashers import make_password
from django.conf import settings
from mongoengine import DoesNotExist
from mongoengine.django.mongo_auth.models import get_user_document
import ldap


class SimpleMongoLDAPBackend(object):
    """
    https://docs.djangoproject.com/en/1.4/topics/auth/#authentication-backends
    """
    user_document = get_user_document()

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
        ldap_uri = settings.AUTH_LDAP_SERVER_URI
        ldap_client = ldap.initialize(ldap_uri)
        try:
            ldap_client.simple_bind_s(user_dn, password)
            user, created = self.get_or_create_user(username)
        except ldap.INVALID_CREDENTIALS:
            pass
        finally:
            ldap_client.unbind()
        return user
