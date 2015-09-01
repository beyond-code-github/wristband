import mock
import pytest

from wristband.apps.providers import NestedReleaseAppDataProvider, ReleaseAppDataProvider

MOCK_RELEASE_APP_RESPONSE = [
    {
        'an': 'a-b-test',
        'env': 'foo-left',
        'ver': '1.7.7',
        'ls': 10,
    },
    {
        'an': 'a-b-test',
        'env': 'bar-left',
        'ver': '1.7.2',
        'ls': 12
    },
    {
        'an': 'a-b-test',
        'env': 'foo-left',
        'ver': '1.7.1',
        'ls': 8
    }
]


@mock.patch.object(NestedReleaseAppDataProvider, '_get_raw_data')
def test_nested_release_app_data_provider(mocked_get_raw_data):
    mocked_get_raw_data.return_value = MOCK_RELEASE_APP_RESPONSE
    expected_response = [
        {
            'name': 'a-b-test',
            'version': '1.7.7',
            'stage': 'foo'
        },
        {
            'name': 'a-b-test',
            'version': '1.7.2',
            'stage': 'bar'
        },
        {
            'name': 'a-b-test',
            'version': '1.7.1',
            'stage': 'foo'
        }
    ]
    assert NestedReleaseAppDataProvider().list_data == expected_response


@mock.patch.object(NestedReleaseAppDataProvider, '_get_raw_data')
def test_nested_release_app_data_provider_filtered_list_data(mocked_get_raw_data):
    mocked_get_raw_data.return_value = MOCK_RELEASE_APP_RESPONSE
    expected_response = [
        {
            'name': 'a-b-test',
            'version': '1.7.2',
            'stage': 'bar'
        },
    ]
    assert NestedReleaseAppDataProvider().get_filtered_list_data(pk='bar', domain_pk='stage') == expected_response


@mock.patch.object(NestedReleaseAppDataProvider, '_get_raw_data')
def test_nested_release_app_data_provider_filtered_list_data_no_result(mocked_get_raw_data):
    mocked_get_raw_data.return_value = MOCK_RELEASE_APP_RESPONSE
    expected_response = []
    assert NestedReleaseAppDataProvider().get_filtered_list_data(pk='test', domain_pk='stage') == expected_response


@mock.patch.object(ReleaseAppDataProvider, '_get_raw_data')
def test_release_app_data_provider(mocked_get_raw_data):
    mocked_get_raw_data.return_value = MOCK_RELEASE_APP_RESPONSE
    expected_response = [
        {
            'name': 'a-b-test',
            'stages': [
                {
                    'name': 'bar',
                    'version': '1.7.2',
                    'job_id': None
                },
                {
                    'name': 'foo',
                    'version': '1.7.7',
                    'job_id': None
                }
            ]
        }
    ]
    provider_under_test = ReleaseAppDataProvider()
    provider_under_test._not_expired_jobs = []
    assert ReleaseAppDataProvider().list_data == expected_response


@pytest.mark.parametrize(('app_name', 'stage', 'expected_response'), [
    ('a-b-test', 'bar', '1234'),
    ('foo', 'bar', None)
])
def test_release_app_data_provider_get_last_job_id_per_app(app_name,
                                                           stage,
                                                           expected_response,
                                                           dummy_app_class,
                                                           dummy_job_class):
    with mock.patch.object(ReleaseAppDataProvider, '_get_raw_data') as mocked_get_raw_data:
        mocked_get_raw_data.return_value = MOCK_RELEASE_APP_RESPONSE
        provider_under_test = ReleaseAppDataProvider()
        provider_under_test._not_expired_jobs = [dummy_job_class(app=dummy_app_class('a-b-test', 'bar'), id='1234'), ]

        assert provider_under_test.get_last_job_id_per_app(app_name, stage) == expected_response
