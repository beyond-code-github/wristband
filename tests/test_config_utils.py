import mock

from config_utils import environments_factory, pipelines_factory

@mock.patch('config_utils.os.getenv')
def test_environment_factory(mock_os_getenv):
    mock_os_getenv.side_effect = lambda environment: {
        "ENVIRONMENTS": "qa-zone_one,qa-zone_two,staging-zone_one,staging-zone_two",
        "ENVIRONMENT_qa_zone_one_jenkins_uri": "https://qa-zone_one",
        "ENVIRONMENT_qa_zone_two_jenkins_uri": "https://qa-zone_two",
        "ENVIRONMENT_staging_zone_one_jenkins_uri": "https://staging-zone_one",
        "ENVIRONMENT_staging_zone_two_jenkins_uri": "https://staging-zone_two",
    }[environment]

    assert environments_factory() == {
        'qa-zone_one': {'jenkins_uri': 'https://qa-zone_one'},
        'qa-zone_two': {'jenkins_uri': 'https://qa-zone_two'},
        'staging-zone_one': {'jenkins_uri': 'https://staging-zone_one'},
        'staging-zone_two': {'jenkins_uri': 'https://staging-zone_two'}
    }


@mock.patch('config_utils.os.getenv')
def test_pipelines_factory(mock_os_getenv):
    mock_os_getenv.side_effect = lambda environment: {
        "PIPELINES": "zone_one,zone_two",
        "PIPELINE_zone_one": "qa-zone_one,staging-zone_one",
        "PIPELINE_zone_two": "qa-zone_one,staging-zone_two",
    }[environment]

    assert pipelines_factory() == {
        'zone_one': ['qa-zone_one', 'staging-zone_one'],
        'zone_two': ['qa-zone_one', 'staging-zone_two']
    }
