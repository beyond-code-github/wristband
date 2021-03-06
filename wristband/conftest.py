from mongoengine.django.mongo_auth.models import get_user_document
import pytest
from rest_framework.test import APIRequestFactory

from wristband.test_utils.authentication import PatchedAPIClient


class DummyApp(object):
    def __init__(self, name, stage=None, security_zone=None):
        self.name = name
        self.stage = stage
        self.security_zone = security_zone


class DummyUser(object):
    def __init__(self, username, pk=1):
        self.pk = self.id = pk
        self.username = username


@pytest.fixture
def dummy_app_class():
    """
    DummyApp class, it's meant to be a quick-and-dirty mock solution for the App document/model

    NOTE: this is the actual class, not an instance
    """
    return DummyApp


@pytest.fixture
def dummy_user_class():
    """
    DummyUser class, it's meant to be a quick-and-dirty mock solution for the User document/model

    NOTE: this is the actual class, not an instance
    """
    return DummyUser


@pytest.fixture
def django_user_model():
    """
    MongoEngine user model as defined in AUTH_USER_MODEL

    Overrides the default pytest-django fixture
    """
    return get_user_document()


@pytest.fixture
def api_client():
    """
    REST framework API client

    This is a patched version using the login function compatible with Mongo
    """
    return PatchedAPIClient()


@pytest.fixture
def api_rf():
    """
    REST framework request factory
    """
    return APIRequestFactory()
