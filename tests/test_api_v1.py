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

@mock.patch('wristband.get_all_releases')
def test_api_config_endpoint(self, all_releases_mock):
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
    expected_data = '{"envs": {"qa": ["qa-zone_one", "qa-zone_two"], "staging": ["staging-zone_one", "staging-zone_two"]}, "apps": [{"envs": {"staging-zone_one": {"versions": [{"ver": "0.4.3", "ls": 18}]}}, "name": "app-1"}, {"envs": {"staging-zone_two": {"versions": [{"ver": "0.0.3", "ls": 10}]}}, "name": "app-2"}], "pipelines": {"zone_two": ["qa-zone_two", "staging-zone_two"], "zone_one": ["qa-zone_one", "staging-zone_one"]}}'
    endpoint = self.app.get('/api/config')
    self.assertEqual(expected_data, endpoint.data)

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
        "event: queued\ndata: {'status': 'OK'}\n\n",
        "event: building\ndata: {'status': 'OK'}\n\n"
        "event: success\ndata: {'status': 'OK'}\n\n"
    ])
    rv = self.app.get('/api/promote/staging-zone_one/my-app/0.0.8')
    self.assertTrue(rv.is_streamed)
    self.assertEquals(rv.content_type, 'text/event-stream')
    self.assertEqual(expected_response, rv.data)
    jenkins_mock.assert_has_calls([mock.call(
        app.app.config['ENVIRONMENTS']["staging-zone_one"]["jenkins_uri"].replace("username:pass@", ""),
        username="username", password="pass")], any_order=True)
