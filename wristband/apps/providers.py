import requests
from django.conf import settings

from wristband.common.providers import JsonDataProvider


class ReleaseAppDataProvider(JsonDataProvider):
    def _get_raw_data(self):
        url = settings.RELEASES_APP_URI
        response = requests.get(url)
        return response.json()

    def _get_list_data(self):
        return [{'name': app['an'],
                 'version': app['ver'],
                 'stage': self.extract_stage_from_env(app['env'])}
                for app in self.raw_data]

    @staticmethod
    def extract_stage_from_env(env):
        return env.split('-')[0]
