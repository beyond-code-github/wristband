import requests
from django.conf import settings

from wristband.common.providers import Provider


class ReleaseAppProvider(Provider):
    def _get_raw_data(self):
        url = settings.RELEASES_APP_URI
        response = requests.get(url)
        return response.json()

    def _get_list_data(self):
        return [{'name': app['an'],
                 'version': app['ver'],
                 'stage': self.extract_stage_from_env(app['env'])}
                for app in self.raw_data]

    def get_retrieve_data(self, pk, lookup_key):
        lookup_key = lookup_key or 'name'
        filtered_data = filter(lambda x: x[lookup_key] == pk, self.list_data)
        data = filtered_data[0] if filtered_data else None
        return data

    @staticmethod
    def extract_stage_from_env(env):
        return env.split('-')[0]
