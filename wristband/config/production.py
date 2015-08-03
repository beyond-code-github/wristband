import os

from config_utils import pipelines_factory, environments_factory


PIPELINES = pipelines_factory()
RELEASES_URI = os.getenv("RELEASES_URI")
ENVIRONMENTS = environments_factory()
