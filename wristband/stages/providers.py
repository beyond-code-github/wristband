from django.conf import settings

from wristband.providers.generics import JsonDataProvider


class EnvVarStagesDataProvider(JsonDataProvider):
    """
    Return the available stages from the env vars

    The data structure needs to match the relevant serializer
    """

    def _get_raw_data(self):
        return settings.STAGES.split(',')

    def _get_list_data(self):
        return [{'name': stage} for stage in self.raw_data]

