from django.conf import settings

from wristband.common.providers import Provider


class EnvVarStagesProvider(Provider):
    """
    Return the available stages from the env vars

    The data structure needs to match the relevant serializer
    """

    def _get_raw_data(self):
        return settings.STAGES.split(',')

    def _get_list_data(self):
        return [{'name': stage} for stage in self.raw_data]

    def get_retrieve_data(self, pk, lookup_key):
        lookup_key = lookup_key or 'name'
        filtered_data = filter(lambda x: x[lookup_key] == pk, self.list_data)
        data = filtered_data[0] if filtered_data else None
        return data

