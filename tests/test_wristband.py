#!/usr/bin/env python

import wristband
import unittest
import json
import mock


class WristbandTestCase(unittest.TestCase):

    def setUp(self):
        wristband.app.config['ENVIRONMENTS'] = {
            "qa-zone_one": {
                "jenkins_uri": "https://qa-zone_one"
            },
            "qa-zone_two": {
                "jenkins_uri": "https://qa-zone_two"
            },
            "staging-zone_one": {
                "jenkins_uri": "https://username:pass@staging-zone_one"
            },
            "staging-zone_two": {
                "jenkins_uri": "https://staging-zone_two"
            },
        }
        wristband.app.config['PIPELINES'] = {
            "zone_one": ["qa-zone_one", "staging-zone_one"],
            "zone_two": ["qa-zone_two", "staging-zone_two"],
        }
        self.app = wristband.app.test_client()

    def test_ping_ping(self):
        rv = self.app.get('/ping/ping')
        self.assertEqual({"status": "OK"}, json.loads(rv.data))

    def notest_api_config_from_app_config(self):
        expected_config = json.loads(wristband.app.config.get('ENVIRONMENTS'))
        rv = self.app.get('/api/config')
        self.assertEqual(expected_config, json.loads(rv.data))

    @mock.patch('requests.get')
    def test_get_env_versions_bad_app_raises_404(self, all_releases_mock):
        all_releases_mock().json = mock.MagicMock(return_value=[
            {
                "an": "test-app",
                "env": "qa",
                "fs": 1437036901,
                "ls": 1437036901,
                "ver": "2.1.3"
            }
        ])
        expected_config = {}
        rv = self.app.get('/api/versions/QA/bad')
        self.assertEqual(404, rv.status_code)

    def test_get_envs_in_pipeline(self):
        pipeline = 'zone_one'
        self.assertEqual(['qa-zone_one', 'staging-zone_one'], wristband.get_envs_in_pipeline(pipeline))

    def test_get_all_releases_of_app_in_env(self):
        deploy_env = "qa"
        app_name = "test-app"
        releases = [
            {
                "an": "test-app",
                "env": "qa",
                "ls": 10,
                "ver": "0.0.3"
            },
            {
                "an": "test-app",
                "env": "qa",
                "ls": 9,
                "ver": "0.0.8"
            },
            {
                "an": "test-app",
                "env": "qa-wrong",
                "ls": 11,
                "ver": "0.0.11"
            },
            {
                "an": "test-app",
                "env": "qa",
                "ls": 8,
                "ver": "0.0.2"
            },
            {
                "an": "test-app-thing",
                "env": "qa",
                "ls": 99,
                "ver": "0.0.99"
            }
        ]
        expected_data = [
            {
                "ls": 10,
                "ver": "0.0.3"
            },
            {
                "ls": 9,
                "ver": "0.0.8"
            },
            {
                "ls": 8,
                "ver": "0.0.2"
            },
        ]
        self.assertEqual(expected_data, wristband.get_all_releases_of_app_in_env(deploy_env, app_name, releases))

    @mock.patch('wristband.get_all_pipelines')
    def test_get_all_environments(self, all_pipelines_mock):
        all_pipelines_mock.return_value =  {
            "zone_one": ["qa-zone_one", "staging-zone_one"],
            "zone_two": ["qa-zone_two", "staging-zone_two"],
        }
        expected_data = ['qa-zone_one', 'qa-zone_two', 'staging-zone_one', 'staging-zone_two']
        self.assertEqual(expected_data, wristband.get_all_environments())

    @mock.patch('wristband.get_all_releases')
    def test_promote_fails_if_not_deployed_to_previous_environment(self, all_releases_mock):
        ### Should this be a SSE????
        all_releases_mock.return_value = [
            {
                "an": "another-app",
                "env": "qa",
                "ls": 10,
                "ver": "0.0.3"
            }
        ]
        rv = self.app.get('/api/promote/staging-zone_one/my-app/0.0.8')
        self.assertEqual(400, rv.status_code)
        self.assertEqual(
            {"error": "you need to deploy 0.0.8 to qa-zone_one first"}, json.loads(rv.data))

    @mock.patch('wristband.Jenkins')
    @mock.patch('wristband.get_all_releases')
    def test_promote_sse_stream(self, all_releases_mock, jenkins_mock):
        all_releases_mock.return_value = [
            {
                "an": "my-app",
                "env": "qa-zone_one",
                "ls": 10,
                "ver": "0.0.8"
            }
        ]
        expected_response = "".join([
            "event: message\ndata: queued\n\n",
            "event: message\ndata: building\n\n"
            "event: message\ndata: success\n\n"
        ])
        rv = self.app.post('/api/promote/staging-zone_one/my-app/0.0.8')
        self.assertTrue(rv.is_streamed)
        self.assertEquals(rv.content_type, 'text/event-stream')
        self.assertEqual(expected_response, rv.data)
        print jenkins_mock.mock_calls
        jenkins_mock.assert_has_calls([mock.call(wristband.app.config['ENVIRONMENTS']["staging-zone_one"]["jenkins_uri"].replace("username:pass@", ""), username="username", password="pass")], any_order=True)



if __name__ == '__main__':
    unittest.main()
