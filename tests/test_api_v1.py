from flask import json, url_for
import mock


@mock.patch('utils.get_all_releases')
def test_promote_fails_if_not_deployed_to_previous_environment(all_releases_mock, client):
    all_releases_mock.return_value = [
        {
            "an": "another-app",
            "env": "qa",
            "ls": 10,
            "ver": "0.0.3"
        }
    ]
    url = url_for('api_v1.promotion', deploy_env='staging-zone_one', app_name='my-app', app_version='0.0.8')
    resource = client.get(url)
    assert resource.status_code == 400
    assert json.loads(resource.data) == {"error": "you need to deploy 0.0.8 to qa-zone_one first"}


@mock.patch('utils.get_all_releases')
@mock.patch('utils.get_all_pipelines')
@mock.patch('utils.get_all_environments')
def test_api_config_endpoint(all_environments, all_pipelines_mock, all_releases_mock, client):
    all_releases_mock.return_value = [
        {
            "an": "app-1",
            "env": "staging-zone_one",
            "ls": 18,
            "ver": "0.4.3"
        },
        {
            "an": "app-2",
            "env": "staging-zone_two",
            "ls": 10,
            "ver": "0.0.3"
        }
    ]

    all_pipelines_mock.return_value = [
        (),
        ()
    ]
    expected_data = '{"envs": {"qa": ["qa-zone_one", "qa-zone_two"], "staging": ["staging-zone_one", "staging-zone_two"]}, "apps": [{"envs": {"staging-zone_one": {"versions": [{"ver": "0.4.3", "ls": 18}]}}, "name": "app-1"}, {"envs": {"staging-zone_two": {"versions": [{"ver": "0.0.3", "ls": 10}]}}, "name": "app-2"}], "pipelines": {"zone_two": ["qa-zone_two", "staging-zone_two"], "zone_one": ["qa-zone_one", "staging-zone_one"]}}'
    resource = client.get(url_for('api_v1.config'))
    assert resource.data == expected_data


@mock.patch('api.v1.Jenkins')
@mock.patch('utils.get_all_releases')
def test_promote_sse_stream(all_releases_mock, jenkins_mock, client):
    all_releases_mock.return_value = [
        {
            "an": "my-app",
            "env": "qa-zone_one",
            "ls": 10,
            "ver": "0.0.8"
        }
    ]
    expected_response = "".join([
        "event: queued\ndata: {'status': 'OK'}\n\n",
        "event: building\ndata: {'status': 'OK'}\n\n"
        "event: success\ndata: {'status': 'OK'}\n\n"
    ])

    url = url_for('api_v1.promotion', deploy_env='staging-zone_one', app_name='my-app', app_version='0.0.8')
    resource = client.get(url)
    assert resource.is_streamed
    assert resource.content_type == 'text/event-stream'
    assert resource.data == expected_response
    jenkins_mock.assert_called_once()
