#!/usr/bin/env python

import unittest
import mock


class WristbandconfigTestCase(unittest.TestCase):
    @mock.patch('os.getenv')
    def test_production_config_mode(self, os_getenv):
        os_getenv.side_effect = lambda environment: {
            "PIPELINES": "zone_one,zone_two",
            "ENVIRONMENTS": "qa-zone_one,qa-zone_two,staging-zone_one,staging-zone_two",
            "ENVIRONMENT_qa_zone_one_jenkins_uri": "https://qa-zone_one",
            "ENVIRONMENT_qa_zone_two_jenkins_uri": "https://qa-zone_two",
            "ENVIRONMENT_staging_zone_one_jenkins_uri": "https://staging-zone_one",
            "ENVIRONMENT_staging_zone_two_jenkins_uri": "https://staging-zone_two",
            "PIPELINE_zone_one": "qa-zone_one,staging-zone_one",
            "PIPELINE_zone_two": "qa-zone_one,staging-zone_two",
            "RELEASES_URI": "http://somewhere/",
        }[environment]
        import wristband.config.production
        self.assertEquals({
            'zone_one': ['qa-zone_one', 'staging-zone_one'],
            'zone_two': ['qa-zone_one', 'staging-zone_two']
        }, wristband.config.production.PIPELINES)

        self.assertEquals({
            'qa-zone_one': {'jenkins_uri': 'https://qa-zone_one'},
            'qa-zone_two': {'jenkins_uri': 'https://qa-zone_two'},
            'staging-zone_one': {'jenkins_uri': 'https://staging-zone_one'},
            'staging-zone_two': {'jenkins_uri': 'https://staging-zone_two'}
        }, wristband.config.production.ENVIRONMENTS)


if __name__ == '__main__':
    unittest.main()
