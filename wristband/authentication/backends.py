import logging
from django.contrib.auth.hashers import make_password

from mongoengine.django.mongo_auth.models import get_user_document
from django_auth_ldap.backend import LDAPBackend, _LDAPUser, populate_user
from rest_framework.authentication import TokenAuthentication
from wristband.authentication.models import Token
from wristband.providers import exceptions

logger = logging.getLogger('wristband.authentication')

# Most of this code comes from django_auth_ldap, I've changed a few lines only to make it work with Mongo
# As soon as the mongo engine team releases the django compatible version this code can go


class LDAPUser(_LDAPUser):
    """
    The user model provided by Mongo Engine doesn't have the set_unusable_password method
    we need to override the method below to handle this
    """
    def _get_or_create_user(self, force_populate=False):
        """
        Loads the User model object from the database or creates it if it
        doesn't exist. Also populates the fields, subject to
        AUTH_LDAP_ALWAYS_UPDATE_USER.
        """
        save_user = False

        username = self.backend.ldap_to_django_username(self._username)
        self._user, created = self.backend.get_or_create_user(username, self)
        self._user.ldap_user = self
        self._user.ldap_username = self._username

        should_populate = force_populate or self.settings.ALWAYS_UPDATE_USER or created

        if created:
            logger.debug("Created Django user %s", username)
            save_user = True

        if should_populate:
            logger.debug("Populating Django user %s", username)
            self._populate_user()
            save_user = True

        if self.settings.MIRROR_GROUPS:
            self._mirror_groups()

        # Give the client a chance to finish populating the user just before
        # saving.
        if should_populate:
            signal_responses = populate_user.send(self.backend.__class__, user=self._user, ldap_user=self)
            if len(signal_responses) > 0:
                save_user = True

        if save_user:
            self._user.save()

        # We populate the profile after the user model is saved to give the
        # client a chance to create the profile. Custom user models in Django
        # 1.5 probably won't have a get_profile method.
        if should_populate and self._should_populate_profile():
            self._populate_and_save_user_profile()


class MongoLDAPBackend(LDAPBackend):
    """
    Need to slightly modify the default one to work with Mongoengine
    """
    def get_user_model(self):
        return get_user_document()

    def get_or_create_user(self, username, ldap_user):
        """
        This must return a (User, created) 2-tuple for the given LDAP user.
        username is the Django-friendly username of the user. ldap_user.dn is
        the user's DN and ldap_user.attrs contains all of their LDAP attributes.
        """

        model = self.get_user_model()
        username_field = getattr(model, 'USERNAME_FIELD', 'username')
        password_field = getattr(model, 'PASSWORD_FIELD', 'password')

        kwargs = {
            username_field: username,
            'defaults': {username_field: username.lower(),
                         password_field: make_password(None)}
        }
        return model.objects.get_or_create(**kwargs)

    def authenticate(self, username, password, **kwargs):
        ldap_user = LDAPUser(self, username=username.strip())
        user = ldap_user.authenticate(password)

        return user


class CustomTokenAuthentication(TokenAuthentication):
    """
    This is REST framework code with minor changes only
    """
    model = Token

    def authenticate_credentials(self, key):
        try:
            token = self.model.objects.get(key=key)
        except self.model.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))

        return token.user, token
