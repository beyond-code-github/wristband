# coding=utf-8

import mock
import pytest
from django.core.exceptions import ImproperlyConfigured

from wristband.providers.config import ProvidersConfig


@mock.patch('django.conf.settings')
def test_providers_config_file_not_found(mock_settings):
    mock_settings.side_effect = IOError
    with pytest.raises(ImproperlyConfigured):
        ProvidersConfig.load_from_file('testfile')


def test_providers_config_invalid_yaml():
    with pytest.raises(ImproperlyConfigured):
        ProvidersConfig.load_from_env('%YAML')
