import pytest

from wristband.common.utils import extract_stage


@pytest.mark.parametrize(('environment', 'expected_result'), [
    ('foo-bar', 'foo'),
    ('test', 'test')
])
def test_extract_stage(environment, expected_result):
    assert extract_stage(environment) == expected_result
