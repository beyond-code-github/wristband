from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.exceptions import APIException


from wristband.common.viewsets import ReadOnlyViewSet
from wristband.providers.exceptions import DeployException
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
        try:
            job_id = provider.deploy(version)
        except DeployException as e:
            raise APIException(e.message)

        return Response({'job_id': job_id})

    def get_permissions(self):
        test_env = getattr(settings, 'TEST_ENV', False)
        if test_env:
            # disable permissions if we're testing
            # I'm aware this is horrible and we should authenticate using the api_client but since we broke the default
            # login function in Django we can't do it and this is quicker (but very nasty!)
            return []
        else:
            super(DeployAppView, self).get_permissions()
