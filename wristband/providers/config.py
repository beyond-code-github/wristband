import binascii

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
import yaml


class ProvidersConfig(object):
    providers = None

    @classmethod
    def load_from_file(cls, filename):
        """
        It assumes the file is in the providers app folder
        """
        try:
            yaml_file = settings.APPS_DIR.path('providers').file(filename)
            cls.providers = yaml.safe_load(yaml_file.read())
            return cls
        except IOError:
            raise ImproperlyConfigured('providers.yaml MUST be provided in the providers app folder')

    @classmethod
    def load_from_env(cls, config):
        """
        Load config from an environment variable.
        We expect YAML in either a Base64-encoded or plaintext string.
        """
        try:
            base64_config = config.decode('base64')
            cls.providers = yaml.safe_load(base64_config)
            return cls
        except binascii.Error:
            cls.providers = yaml.safe_load(config)
            return cls
        except yaml.YAMLError:
            raise ImproperlyConfigured('PROVIDER_CONFIG must be valid YAML, and Base64-encoded or plaintext')
