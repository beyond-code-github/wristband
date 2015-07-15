#!/usr/bin/env python

import wristband
import unittest
import json


class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        wristband.app.config['ENVS'] = json.dumps({
            "envs": {
                "QA": [
                    "qa-left",
                    "qa-right",
                ],
                "staging": [
                    "staging-left",
                    "staging-right",
                ]
            },
            "apps": [
                "test-fe-1",
                "test-be-5",
            ]
        })
        self.app = wristband.app.test_client()

    def test_ping_ping(self):
        rv = self.app.get('/ping/ping')
        self.assertEqual({"status": "OK"}, json.loads(rv.data))

    def test_api_config_from_app_config(self):
        expected_config = json.loads(wristband.app.config.get('ENVS'))
        rv = self.app.get('/api/config')
        self.assertEqual(expected_config, json.loads(rv.data))

    def test_get_env_versions_bad_app_raises_404(self):
        expected_config = {}
        rv = self.app.get('/api/versions/QA/bad')
        self.assertEqual(404, rv.status_code)

    #def test_api_config_from_app_config(self):
    #    expected_config = {}
    #    rv = self.app.get('/api/versions/qa-left/captain')
    #    self.assertEqual(expected_config, json.loads(rv.data))


if __name__ == '__main__':
    unittest.main()
