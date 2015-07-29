from wristband.utils import Release, Environment

releases_test_data = [
    (
        {
            'an': 'test_name',
            'env': 'test_environment',
            'fs': 'test_first_seen',
            'ls': 'test_last_seen',
            'ver': 'test_version'
        }
    ), (
        {
            'an': 'test_name',
            'env': 'test_environment',
            'fs': 'test_first_seen',
            'ls': 'test_last_seen',
            'ver': 'test_version',
            'not_converted': 'test_not_converted'
        }
    )
]

def test_release_creation_from_dictionary():
    def check_creation(dictionary):
        release_under_test = Release.from_dictionary(dictionary)
        for key in dictionary:
            try:
                class_attribute = release_under_test.mapping_keys[key]
            except KeyError:
                class_attribute = key
            assert getattr(release_under_test, class_attribute) == dictionary[key]

    for dictionary in releases_test_data:
        yield check_creation, dictionary


environments_test_data = [
    ('qa-left', 'qa-left', 'qa', 'left'),
    ('dev', 'dev', 'dev', 'dev')
]

def test_environment_creation_from_environment_name():
    def check_creation(env_name, expected_name, expected_left, expected_right):
        environment_under_test = Environment.from_environment_name(env_name)
        assert environment_under_test.name == expected_name
        assert environment_under_test.left == expected_left
        assert environment_under_test.right == expected_right
        assert environment_under_test.jenkins_uri == None

    for env_name, expected_name, expected_left, expected_right in environments_test_data:
        yield check_creation, env_name, expected_name, expected_left, expected_right