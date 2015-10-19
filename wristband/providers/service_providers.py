import logging

from django.conf import settings
import requests
from requests import HTTPError

from . import providers_config
from .generics import ServiceProvider
from wristband.apps.models import App
from wristband.providers.exceptions import DeployException

logger = logging.getLogger('wristband.provider')


class DocktorServiceProvider(ServiceProvider):
    def __init__(self, app_name, stage):
        self.app = App.objects.get(name=app_name)
        self.stage = stage
        self.config = self.get_docktor_server_config()
        self.app_url = "{uri}/apps/{app_name}".format(uri=self.config["uri"], app_name=self.app.name)

    def get_docktor_server_config(self):
        return providers_config.providers['docktor'][self.stage][self.app.security_zone]

    def deploy(self, version):
        try:
            params ={"slug_uri": "{webstore_url}/{app}/{app}_{version}.tgz".format(
                    webstore_url=settings.WEBSTORE_URL,
                    app=self.app_name,
                    version=version)}
            r = requests.patch(self.app_url, data=params)
            r.raise_for_status()
        except HTTPError as e:
            raise DeployException(e.message)

