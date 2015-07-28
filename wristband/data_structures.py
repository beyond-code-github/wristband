import re

class Release(object):

    mapping_keys = {
        'an': 'app_name',
        'env': 'environment',
        'fs': 'first_seen',
        'ls': 'last_seen',
        'ver': 'version'
    }


    @classmethod
    def from_dictionary(cls, dictionary):
        for key, value in dictionary.iteritems():
            setattr(cls, cls.mapping_keys.get(key, key), value)
        return cls


class Environment(object):

    regex = r'^((?P<left>\w+)-(?P<right>\w+))$|^(?P<name>\w+)$'

    def __init__(self, name, left, right):
        self.name = name
        self.left = left
        self.right = right

    @classmethod
    def from_string(cls, env_name):
        cls._parse_name(env_name)
        return cls

    def _parse_name(self, env_name):
        m = re.search(self.regex, env_name)
        self.right = m.group('right') or env_name
        self.left = m.group('left') or env_name