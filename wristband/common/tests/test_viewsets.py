import pytest

from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.serializers import Serializer, CharField

from wristband.common.viewsets import ReadOnlyViewSet
from wristband.providers.generics import DataProvider

EMPTY_REQUEST = {}
PK = 'test'


class DummySerializer(Serializer):
    """
    It's easier to create a simple Serializer than trying to use Mock in this case
    """
    name = CharField()


class DummyProvider(DataProvider):
    def _get_list_data(self):
        return [{'name': 'test1'}, {'name': 'test2'}]

    def _get_raw_data(self):
        return [{'name': 'test1'}, {'name': 'test2'}]

    def get_retrieve_data(self, pk, *args, **kwargs):
        """
        FIXME For some reason the mixin providing this code doesn't seem to work in the tests
        This needs more investigation
        """
        filtered_data = filter(lambda x: x['name'] == pk, self.list_data)
        data = filtered_data[0] if filtered_data else None
        return data


def test_read_only_view_set_list():
    viewset_under_test = ReadOnlyViewSet()
    viewset_under_test.serializer_class = DummySerializer
    viewset_under_test.data_provider_class = DummyProvider

    assert isinstance(viewset_under_test.list(EMPTY_REQUEST), Response)


def test_read_only_view_set_retrieve_data_found():
    viewset_under_test = ReadOnlyViewSet()
    viewset_under_test.serializer_class = DummySerializer
    viewset_under_test.data_provider_class = DummyProvider

    assert isinstance(viewset_under_test.retrieve(EMPTY_REQUEST, 'test1'), Response)


def test_read_only_view_set_retrieve_data_not_found():
    viewset_under_test = ReadOnlyViewSet()
    viewset_under_test.serializer_class = DummySerializer
    viewset_under_test.data_provider_class = DummyProvider

    with pytest.raises(NotFound):
        response = viewset_under_test.retrieve(EMPTY_REQUEST, 'test3')
        assert response.status_code == 404