from rest_framework.response import Response
from rest_framework.views import APIView

from wristband.common.viewsets import ReadOnlyViewSet
from .providers import NestedReleaseAppDataProvider, ReleaseAppDataProvider
from .serializers import NestedAppSerializer, AppSerializer


class NestedAppViewSet(ReadOnlyViewSet):
    serializer_class = NestedAppSerializer
    data_provider_class = NestedReleaseAppDataProvider


class AppViewSet(ReadOnlyViewSet):
    serializer_class = AppSerializer
    data_provider_class = ReleaseAppDataProvider


class DeployAppView(APIView):
    def put(self, request, format=None):
        return Response('Hello')
