from functools import partial

import requests
from gevent import monkey;

monkey.patch_socket()
from gevent.pool import Pool

from wristband.common.utils import extract_version_from_slug
from wristband.providers import providers_config
from wristband.providers.generics import JsonDataProvider

EXPIRY_JOB_TIME_MINUTES = 10
CONCURRENT_JOBS_LIMIT = 30


class GenericDocktorDataProvider(JsonDataProvider):
    def _get_raw_data(self):
        docktor_config = providers_config.providers['docktor']
        apps = []
        for stage in docktor_config:
            for zone in docktor_config[stage]:
                apps_uri = '{uri}/apps/'.format(uri=docktor_config[stage][zone]['uri'])
                apps_list = requests.get(apps_uri).json()
                apps_urls = ['{apps_uri}{app}'.format(apps_uri=apps_uri, app=app) for app in apps_list]
                pool = Pool(CONCURRENT_JOBS_LIMIT)
                partial_get_app_info = partial(self.get_app_info, stage)
                apps += pool.map(partial_get_app_info, apps_urls)
        return apps

    @staticmethod
    def get_app_info(stage, env_url):
        data = requests.get(env_url).json()
        return {
            'name': data['app'],
            'stage': stage,
            'version': extract_version_from_slug(data['slug_uri']),
            'state': data['state']
        }


class NestedDocktorAppDataProvider(GenericDocktorDataProvider):
    def _get_list_data(self):
        """
        Show only the latest version per stage, filter by last seen
        """
        data = [{'name': app['name'],
                 'version': app['version'],
                 'stage': app['stage'],
                 'state': app['state']}
                for app in self.raw_data]
        return sorted(data, key=lambda x: x['name'])

    def get_filtered_list_data(self, pk, domain_pk):
        filtered_apps = filter(lambda x: x[domain_pk] == pk, self.list_data)
        return sorted(filtered_apps, key=lambda x: x['name'])


class DocktorAppDataProvider(GenericDocktorDataProvider):
    def _get_list_data(self):
        """
        We need to get this format from the current releases app format

        Docktor output:
        [
            {
                "name": "a-b-test",
                "environment": "qa-left",
                "version": "1.7.7"
                "state": "healthy"
            },
            {
                "name": "a-b-test",
                "environment": "staging-left",
                "version": "1.7.2"
                "state": "unhealthy"
            }
        ]

        Expected output:
        [
            {
                "name": "a-b-test",
                    "stages": [
                        {
                           "name": "qa",
                           "version": "1.7.7"
                           "state": "healthy"
                        },
                        {
                           "name": "staging",
                           "version": "1.7.2"
                           "state": "unhealthy"
                        }
                    ]
            },
            {...}
        ]
        """
        data = []
        apps_indexes = {}
        for app in self.raw_data:
            app_name = app['name']
            app_stage = app['stage']
            if app_name in apps_indexes.keys():
                # we've already seen this app
                already_seen_app_index = apps_indexes[app_name]
                data[already_seen_app_index]['stages'].append({
                    'name': app_stage,
                    'version': app['version'],
                    'state': app['state']
                })
            else:
                # we've never seen this app before
                app_to_be_added = {
                    'name': app_name,
                    'stages': [{
                        'name': app_stage,
                        'version': app['version'],
                        'state': app['state']
                    }]
                }
                data.append(app_to_be_added)
                apps_indexes[app_name] = len(data) - 1
        return sorted(data, key=lambda x: x['name'])
