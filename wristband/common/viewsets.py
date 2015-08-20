from rest_framework.exceptions import NotFound
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response


class ReadOnlyViewSet(ViewSet):
    """
    Parent Read Only ViewSet class, it only implements GET
    """
    serializer_class = None
    data_provider_class = None

    def list(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self._get_list_data(), many=True)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data)

    def retrieve(self, request, pk, lookup_key=None, *args, **kwargs):
        data = self._get_retrieve_data(pk, lookup_key)
        if data:
            serializer = self.serializer_class(data=data)
            if serializer.is_valid(raise_exception=True):
                return Response(serializer.data)
        else:
            raise NotFound()

    def _get_list_data(self):
        return self.data_provider_class().list_data

    def _get_retrieve_data(self, pk, lookup_key):
        return self.data_provider_class().get_retrieve_data(pk, lookup_key)
