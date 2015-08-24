import pytest

from wristband.common.mixins import JsonDataProviderRetrieveMixin

@pytest.mark.parametrize(('list_data', 'pk', 'lookup_key', 'expected_result'), [
    (
        [{'name': 'test1', 'version': 1}, {'name': 'test2', 'version': 2}],
        'test1',
        None,
        {'name': 'test1', 'version': 1}
    ),
    (
        [{'name': 'test1', 'version': 1}, {'name': 'test2', 'version': 2}],
        2,
        'version',
        {'name': 'test2', 'version': 2}
    ),
    (
        [{'name': 'test1', 'version': 1}, {'name': 'test2', 'version': 2}],
        'test3',
        'name',
        None
    ),
])
def test_json_data_provider_retrieve_mixin_retrieve_data(list_data, pk, lookup_key, expected_result):
    mixin_under_test = JsonDataProviderRetrieveMixin()
    mixin_under_test.list_data = list_data
    assert mixin_under_test.get_retrieve_data(pk, lookup_key) == expected_result
