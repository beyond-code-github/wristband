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

    def get_filtered_list_data(self, pk, domain_pk):
        """
        Return a list of filtered objects
        """
        pass

    def get_retrieve_data(self, pk, domain_pk):
        """
        Return a single object, looked up by the passed pk
        """
        raise NotImplementedError('The method get_retrieve_data must be implemented')


class JsonDataProvider(JsonDataProviderRetrieveMixin, DataProvider):
  pass


class ServiceProvider(object):
    config = None

    def __init__(self, app_name, stage):
        raise NotImplementedError('The method __init__ must be implemented')

    def deploy(self, version):
        raise NotImplementedError('The method promote must be implemented')

    def status(self, job_id):
        raise NotImplementedError('The method status must be implemented')

    def save_job_info(self, version):
        raise NotImplementedError('The method save_job_info must be implemented')
