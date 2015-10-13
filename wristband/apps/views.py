from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.exceptions import APIException

from wristband.common.viewsets import ReadOnlyViewSet
from wristband.providers.exceptions import DeployException
from wristband.providers.service_providers import DocktorServiceProvider
from .providers import NestedDocktorAppDataProvider, DocktorAppDataProvider
from .serializers import NestedAppSerializer, AppSerializer


class NestedAppViewSet(ReadOnlyViewSet):
    serializer_class = NestedAppSerializer
    data_provider_class = NestedDocktorAppDataProvider

    def list(self, request, *args, **kwargs):
        stage_pk = kwargs['stage_pk']
        serializer = self.serializer_class(data=self._get_filtered_list_data(pk=stage_pk, lookup_key='stage'),
                                           many=True)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data)


class AppViewSet(ReadOnlyViewSet):
    serializer_class = AppSerializer
    data_provider_class = DocktorAppDataProvider


class DeployAppView(APIView):
    permission_classes = (IsAdminUser,)

    def put(self, request, app_name, stage, version, format=None):
        provider = DocktorServiceProvider(app_name, stage)
        try:
            job_id = provider.deploy(version)
        except DeployException as e:
            raise APIException(e.message)

        return Response({'job_id': job_id})
