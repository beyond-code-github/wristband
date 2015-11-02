from functools import partial

from requests_futures.sessions import FuturesSession
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from django.conf import settings

from wristband.common.utils import extract_version_from_slug
from wristband.providers import providers_config
from wristband.providers.generics import JsonDataProvider

import logging
logger = logging.getLogger('wristband.apps.providers')

CONCURRENT_JOBS_LIMIT = 10
REQUEST_TIMEOUT = 10
REQUEST_RETRIES = 10


class GenericDocktorDataProvider(JsonDataProvider):
    __requests_http_adapter = HTTPAdapter(
        Retry(total=REQUEST_RETRIES, status_forcelist=[502], backoff_factor=0.5))

    def _get_raw_data(self):
        docktor_config = providers_config.providers['docktor']
        apps = []
        session = FuturesSession(max_workers=CONCURRENT_JOBS_LIMIT)
        session.mount('https://', self.__requests_http_adapter)
        session.mount('http://', self.__requests_http_adapter)
        for stage in docktor_config:
            for zone in docktor_config[stage]:
                apps_uri = '{uri}/apps/'.format(uri=docktor_config[stage][zone]['uri'])
                try:
                    r = session.get(apps_uri, timeout=REQUEST_TIMEOUT).result()
                    r.raise_for_status()
                    apps_list = r.json()
                except ValueError as e:
                    logger.error("Non json response {} from {}-{} docktor".format(r.content, stage, zone))
                    raise e
                except Exception as e:
                    logger.error("Exception raised on {}-{} docktor".format(stage, zone))
                    raise e

                future_apps_details = [session.get('{apps_uri}{app}'.format(apps_uri=apps_uri, app=app), timeout=REQUEST_TIMEOUT) for app in apps_list]

                try:
                    apps_details = [a.result() for a in future_apps_details]
                except Exception as e:
                    logger.error("Exception raised on {}-{} docktor".format(stage, zone))
                    raise e

                partial_get_app_info = partial(self.get_app_info, stage, zone)

                apps.extend(map(lambda a: partial_get_app_info(a), apps_details))
        return apps

    @staticmethod
    def get_app_info(stage, zone, response):
        try:
            response.raise_for_status()
        except ValueError as e:
            logger.error("Non json response {} from {}-{} docktor".format(response.content, stage, zone))
            raise e
        data = response.json()
        return {
            'name': data['app'],
            'stage': stage,
            'security_zone': zone,
            'version': extract_version_from_slug(data['slug_uri']),
            'state': data['state'],
            'log_url': settings.KIBANA_URL.format(stage=stage, security_zone=zone)
        }


class NestedDocktorAppDataProvider(GenericDocktorDataProvider):
    def _get_list_data(self):
        """
        Show only the latest version per stage, filter by last seen
        """
        data = [{'name': app['name'],
                 'version': app['version'],
                 'stage': app['stage'],
                 'state': app['state'],
                 'log_url': app['log_url']}
                for app in self.raw_data]
        return sorted(data, key=lambda x: x['name'])

    def get_filtered_list_data(self, pk, domain_pk):
        filtered_apps = filter(lambda x: x[domain_pk] == pk, self.list_data)
        return sorted(filtered_apps, key=lambda x: x['name'])

    def to_models(self):
        return [{'name': app['name'],
                 'stage': app['stage'],
                 'security_zone': app['security_zone']}
                for app in self.raw_data]


class DocktorAppDataProvider(GenericDocktorDataProvider):
    def _get_list_data(self):
        """
        We need to get this format from the current releases app format

        Docktor output:
        [
            {
                "name": "a-b-test",
                "stage": "qa",
                "version": "1.7.7"
                "state": "healthy"
            },
            {
                "name": "a-b-test",
                "stage": "staging",
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
                           "state": "healthy",
                           "log_url": none
                        },
                        {
                           "name": "staging",
                           "version": "1.7.2"
                           "state": "unhealthy",
                           "log_url": "https://test.com/#/dashboard/file/deployments.json?microservice=wristband"
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
                    'state': app['state'],
                    'log_url': app['log_url']

                })
            else:
                # we've never seen this app before
                app_to_be_added = {
                    'name': app_name,
                    'stages': [{
                        'name': app_stage,
                        'version': app['version'],
                        'state': app['state'],
                        'log_url': app['log_url']
                    }]
                }
                data.append(app_to_be_added)
                apps_indexes[app_name] = len(data) - 1
        return sorted(data, key=lambda x: x['name'])
