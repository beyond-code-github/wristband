import mock
import pytest

from wristband.apps.providers import NestedDocktorAppDataProvider, DocktorAppDataProvider

MOCK_DOCKTOR_RESPONSE = [
    {
        'name': 'a-b-test',
        'stage': 'foo',
        'version': '1.7.7',
        'state': 'healthy',
        'log_url': None
    },
    {
        'name': 'a-b-test',
        'stage': 'bar',
        'version': '1.7.2',
        'state': 'unhealthy',
        'log_url': ''
    }
]

KIBANA_URL = 'https://{stage}-{security_zone}.test.com'


@pytest.mark.parametrize(('app_data', 'stage', 'security_zone', 'expected_result'), [
    (
        {
            'app': 'a-b-test',
            'slug_uri': 'https://test.com/slugs/a-b-test_1.7.7.tgz',
            'state': 'healthy'
        },
        'foo',
        'bar',
        {
            'name': 'a-b-test',
            'stage': 'foo',
            'security_zone': 'bar',
            'version': '1.7.7',
            'state': 'healthy',
            'log_url': 'https://foo-bar.test.com'
        }
    ),
    (
         {
            'app': 'a-b-test',
            'slug_uri': 'https://test.com/slugs/a-b-test_1.7.2.tgz',
            'state': 'unhealthy'
        },
        'foo',
        'bar',
        {
            'name': 'a-b-test',
            'stage': 'foo',
            'security_zone': 'bar',
            'version': '1.7.2',
            'state': 'unhealthy',
            'log_url': 'https://foo-bar.test.com'
        }
    )
])
def test_get_app_info(app_data, stage, security_zone,  expected_result, settings):
    settings.KIBANA_URL = KIBANA_URL
    with mock.patch('wristband.apps.providers.FuturesSession') as mocked_requests:
        mocked_requests.json.return_value = app_data
        assert NestedDocktorAppDataProvider.get_app_info(stage, security_zone, mocked_requests) == expected_result


@mock.patch.object(NestedDocktorAppDataProvider, '_get_raw_data')
def test_nested_release_app_data_provider_list_data(mocked_get_raw_data, settings):
    mocked_get_raw_data.return_value = MOCK_DOCKTOR_RESPONSE
    settings.KIBANA_URL = KIBANA_URL
    expected_response = [
        {
            'name': 'a-b-test',
            'version': '1.7.7',
            'stage': 'foo',
            'state': 'healthy',
            'log_url': None
        },
        {
            'name': 'a-b-test',
            'version': '1.7.2',
            'stage': 'bar',
            'state': 'unhealthy',
            'log_url': ''
        },
    ]
    assert NestedDocktorAppDataProvider().list_data == expected_response


@mock.patch.object(NestedDocktorAppDataProvider, '_get_raw_data')
def test_nested_release_app_data_provider_filtered_list_data(mocked_get_raw_data, settings):
    mocked_get_raw_data.return_value = MOCK_DOCKTOR_RESPONSE
    settings.KIBANA_URL = KIBANA_URL
    expected_response = [
        {
            'name': 'a-b-test',
            'version': '1.7.2',
            'stage': 'bar',
            'state': 'unhealthy',
            'log_url': ''
        },
    ]
    assert NestedDocktorAppDataProvider().get_filtered_list_data(pk='bar', domain_pk='stage') == expected_response


@mock.patch.object(NestedDocktorAppDataProvider, '_get_raw_data')
def test_nested_release_app_data_provider_filtered_list_data_no_result(mocked_get_raw_data):
    mocked_get_raw_data.return_value = MOCK_DOCKTOR_RESPONSE
    expected_response = []
    assert NestedDocktorAppDataProvider().get_filtered_list_data(pk='test', domain_pk='stage') == expected_response


@mock.patch.object(DocktorAppDataProvider, '_get_raw_data')
def test_release_app_data_provider(mocked_get_raw_data, settings):
    settings.KIBANA_URL = KIBANA_URL
    mocked_get_raw_data.return_value = MOCK_DOCKTOR_RESPONSE
    expected_response = [
        {
            'name': 'a-b-test',
            'stages': [
                {
                    'name': 'foo',
                    'version': '1.7.7',
                    'state': 'healthy',
                    'log_url': None
                },
                {
                    'name': 'bar',
                    'version': '1.7.2',
                    'state': 'unhealthy',
                    'log_url': ''
                }
            ]
        }
    ]
    provider_under_test = DocktorAppDataProvider()
    provider_under_test._not_expired_jobs = []
    assert DocktorAppDataProvider().list_data == expected_response
