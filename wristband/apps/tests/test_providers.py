import mock

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


@mock.patch.object(ReleaseAppDataProvider, '_get_raw_data')
def test_release_app_data_provider(mocked_get_raw_data):
    mocked_get_raw_data.return_value = MOCK_RELEASE_APP_RESPONSE
    expected_response = [
        {
            'name': 'a-b-test',
                'stages': [
                    {
                       'name': 'bar',
                       'version': '1.7.2'
                    },
                    {
                       'name': 'foo',
                       'version': '1.7.7'
                    }
                ]
        }
    ]
    assert ReleaseAppDataProvider().list_data == expected_response
