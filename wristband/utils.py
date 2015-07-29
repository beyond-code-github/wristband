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
    """
    Left and right may add more confusion, but the just refer to what's
    before and after the -.
    If there not left or right then the full environment name is used
    Better names suggestion are welcome

    """
    regex = r'^((?P<left>\w+)-(?P<right>\w+))$|^(?P<name>\w+)$'

    def __init__(self, name, left, right, jenkins_uri):
        self.name = name
        self.left = left
        self.right = right
        self.jenkins_uri = jenkins_uri

    @classmethod
    def from_environment_name(cls, env_name):
        m = re.search(cls.regex, env_name)
        cls.right = m.group('right') or env_name
        cls.left = m.group('left') or env_name
        cls.name = env_name
        cls.jenkins_uri = None
        return cls
