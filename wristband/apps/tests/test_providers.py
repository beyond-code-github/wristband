import mock

from wristband.apps.providers import NestedDocktorAppDataProvider, DocktorAppDataProvider

MOCK_DOCKTOR_RESPONSE = [
    {
        'name': 'a-b-test',
        'stage': 'foo',
        'version': '1.7.7',
        'state': 'healthy'
    },
    {
        'name': 'a-b-test',
        'stage': 'bar',
        'version': '1.7.2',
        'state': 'unhealthy'
    }
]


@mock.patch.object(NestedDocktorAppDataProvider, '_get_raw_data')
def test_nested_release_app_data_provider_list_data(mocked_get_raw_data):
    mocked_get_raw_data.return_value = MOCK_DOCKTOR_RESPONSE
    expected_response = [
        {
            'name': 'a-b-test',
            'version': '1.7.7',
            'stage': 'foo',
            'state': 'healthy'
        },
        {
            'name': 'a-b-test',
            'version': '1.7.2',
            'stage': 'bar',
            'state': 'unhealthy'
        },
    ]
    assert NestedDocktorAppDataProvider().list_data == expected_response


@mock.patch.object(NestedDocktorAppDataProvider, '_get_raw_data')
def test_nested_release_app_data_provider_filtered_list_data(mocked_get_raw_data):
    mocked_get_raw_data.return_value = MOCK_DOCKTOR_RESPONSE
    expected_response = [
        {
            'name': 'a-b-test',
            'version': '1.7.2',
            'stage': 'bar',
            'state': 'unhealthy'
        },
    ]
    assert NestedDocktorAppDataProvider().get_filtered_list_data(pk='bar', domain_pk='stage') == expected_response


@mock.patch.object(NestedDocktorAppDataProvider, '_get_raw_data')
def test_nested_release_app_data_provider_filtered_list_data_no_result(mocked_get_raw_data):
    mocked_get_raw_data.return_value = MOCK_DOCKTOR_RESPONSE
    expected_response = []
    assert NestedDocktorAppDataProvider().get_filtered_list_data(pk='test', domain_pk='stage') == expected_response


@mock.patch.object(DocktorAppDataProvider, '_get_raw_data')
def test_release_app_data_provider(mocked_get_raw_data):
    mocked_get_raw_data.return_value = MOCK_DOCKTOR_RESPONSE
    expected_response = [
        {
            'name': 'a-b-test',
            'stages': [
                {
                    'name': 'foo',
                    'version': '1.7.7',
                    'state': 'healthy'
                },
                {
                    'name': 'bar',
                    'version': '1.7.2',
                    'state': 'unhealthy'
                }
            ]
        }
    ]
    provider_under_test = DocktorAppDataProvider()
    provider_under_test._not_expired_jobs = []
    assert DocktorAppDataProvider().list_data == expected_response
