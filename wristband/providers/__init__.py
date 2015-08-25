from django.core.exceptions import ImproperlyConfigured
import yaml

from django.conf import settings


class ProvidersConfig(object):
    providers = None

    @classmethod
    def load_from_file(cls, filename):
        """
        It assumes the file is in the providers app folder
        """
        try:
            yaml_file = settings.APPS_DIR.path('providers').file(filename)
            cls.providers = yaml.load(yaml_file.read())
            return cls
        except IOError:
            raise ImproperlyConfigured('providers.yaml MUST be provided in the providers app folder')


providers_config = ProvidersConfig.load_from_file('providers.yaml')
