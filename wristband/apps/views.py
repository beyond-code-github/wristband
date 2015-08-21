from wristband.common.viewsets import ReadOnlyViewSet

from .providers import ReleaseAppDataProvider
from .serializers import AppSerializer

class AppViewSet(ReadOnlyViewSet):
    serializer_class = AppSerializer
    data_provider_class = ReleaseAppDataProvider
