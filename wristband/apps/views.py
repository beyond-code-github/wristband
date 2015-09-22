from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser

from wristband.common.viewsets import ReadOnlyViewSet
from wristband.providers.service_providers import JenkinsServiceProvider
from .providers import NestedReleaseAppDataProvider, ReleaseAppDataProvider
from .serializers import NestedAppSerializer, AppSerializer


class NestedAppViewSet(ReadOnlyViewSet):
    serializer_class = NestedAppSerializer
    data_provider_class = NestedReleaseAppDataProvider

    def list(self, request, *args, **kwargs):
        stage_pk = kwargs['stage_pk']
        serializer = self.serializer_class(data=self._get_filtered_list_data(pk=stage_pk, lookup_key='stage'),
                                           many=True)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data)


class AppViewSet(ReadOnlyViewSet):
    serializer_class = AppSerializer
    data_provider_class = ReleaseAppDataProvider


class DeployAppView(APIView):
    permission_classes = (IsAdminUser,)

    def put(self, request, app_name, stage, version, format=None):
        provider = JenkinsServiceProvider(app_name, stage)
        job_id = provider.deploy(version)
        return Response({'job_id': job_id})
