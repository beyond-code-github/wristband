import pytest

class DummyApp(object):
    def __init__(self, name, stage=None, security_zone=None):
        self.name = name
        self.stage = stage
        self.security_zone = security_zone


class DummyJob(object):
    def __init__(self, app, id):
        self.app = app
        self.id = id


@pytest.fixture
def dummy_app_class():
    return DummyApp


@pytest.fixture
def dummy_job_class():
    return DummyJob