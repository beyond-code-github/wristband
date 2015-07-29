import os

from .utils import pipelines_factory, environments_factory


PIPELINES = pipelines_factory()
RELEASES_URI = os.getenv("RELEASES_URI")
ENVIRONMENTS = environments_factory()
