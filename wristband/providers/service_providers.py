import logging
import json

import requests

from . import providers_config
from .generics import ServiceProvider
from wristband.providers.exceptions import DeployException

JENKINS_CALL_SAFE_LIMIT = 8

logger = logging.getLogger('wristband.provider')


class DocktorServiceProvider(ServiceProvider):
    def __init__(self, app_name, environment):
        self.app_name = app_name
        self.config = self.get_docktor_server_config()
        self.server = requests.session()

    def get_docktor_server_config(self):
        return providers_config.providers['docktor'][self.app.stage][self.app.security_zone]

    def deploy(self, version):
        params = {
            "APP": self.app.name,
            "APP_BUILD_NUMBER": version
        }
        try:
            r = self.server.patch("{}/apps/{}".format(self.config["uri"], self.app_name),
                                  headers={"content-type": "application/json"}, data=json.dumps({
                                                                                                    "slug_uri": "https://webstore.tax.service.gov.uk/slugs/{app}/{app}_{version}.tgz".format(
                                                                                                        app=self.app_name,
                                                                                                        version=version)}))
            r.raise_for_status()
        except requests.HTTPError as e:
            raise DeployException(e.message)
        return self.save_job_info(version)

    def status(self, job):
        build_info = self.server.get("{}/apps/{}".format(self.config.url, self.app)).json()
        return build_info['state']
