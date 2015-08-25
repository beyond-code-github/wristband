from wristband.common.mixins import JsonDataProviderRetrieveMixin

class DataProvider(object):
    """
    Read-only data provider
    """
    def __init__(self):
        self.raw_data = self._get_raw_data()
        self.list_data = self._get_list_data()

    def _get_raw_data(self):
        raise NotImplementedError('The method _get_raw_data must be implemented')

    def _get_list_data(self):
        """
        Return a list of objects
        """
        raise NotImplementedError('The method _get_list_data must be implemented')

    def get_retrieve_data(self, pk, domain_pk):
        """
        Return a single object, looked up by the passed pk
        """
        raise NotImplementedError('The method get_retrieve_data must be implemented')


class JsonDataProvider(DataProvider, JsonDataProviderRetrieveMixin):
    pass


class ServiceProvider(object):
    config = None

    def promote(self, version):
        raise NotImplementedError('The method promote must be implemented')

    def status(self, job_id):
        pass
