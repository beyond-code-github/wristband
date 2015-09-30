import pytest
import mock

from wristband.common.utils import extract_stage, extract_security_zone_from_env, get_security_zone_from_app_name, \
    extract_version_from_slug


@pytest.mark.parametrize(('environment', 'expected_result'), [
    ('foo-bar', 'foo'),
    ('dev', 'dev')
])
def test_extract_stage(environment, expected_result):
    assert extract_stage(environment) == expected_result


@pytest.mark.parametrize(('environment', 'expected_result'), [
    ('foo-bar', 'bar'),
    ('dev', 'dev')
])
def test_extract_security_zone_from_env(environment, expected_result):
    assert extract_security_zone_from_env(environment) == expected_result


def test_get_security_zone_from_app_name_app_found(dummy_app_class):
    with mock.patch('wristband.common.utils.App') as mocked_app:
        mocked_objects_method = mock.Mock()
        mocked_objects_method.first.return_value = dummy_app_class(name='foo', security_zone='bar')
        mocked_app.objects.return_value = mocked_objects_method

        assert get_security_zone_from_app_name('foo') == 'bar'


def test_get_security_zone_from_app_name_app_not_found():
    with mock.patch('wristband.common.utils.App') as mocked_app:
        mocked_objects_method = mock.Mock()
        mocked_objects_method.first.return_value = []
        mocked_app.objects.return_value = mocked_objects_method

        assert get_security_zone_from_app_name('foo') is None


@pytest.mark.parametrize(('slug', 'expected_result'), [
    ('foo_2.6.4', '2.6.4'),
    ('fdfds', '')
])
def test_extract_version_from_slug(slug, expected_result):
    assert extract_version_from_slug(slug) == expected_result
