import pytest

from wristband.common.utils import extract_stage, extract_security_zone_from_env, extract_version_from_slug


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


@pytest.mark.parametrize(('slug', 'expected_result'), [
    ('foo_2.6.4.tgz', '2.6.4'),
    ('fdfds', '')
])
def test_extract_version_from_slug(slug, expected_result):
    assert extract_version_from_slug(slug) == expected_result
