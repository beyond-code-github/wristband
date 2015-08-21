class JsonDataProviderRetrieveMixin(object):
    def get_retrieve_data(self, pk, lookup_key):
        lookup_key = lookup_key or 'name'
        filtered_data = filter(lambda x: x[lookup_key] == pk, self.list_data)
        data = filtered_data[0] if filtered_data else None
        return data
