from wristband.common.viewsets import ReadOnlyViewSet

from .serializers import StageSerializer
from .providers import EnvVarStagesDataProvider


class StagesViewSet(ReadOnlyViewSet):
    serializer_class = StageSerializer
    data_provider_class = EnvVarStagesDataProvider
