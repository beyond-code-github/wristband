# config.py

import os

__environment_list = os.getenv("ENVIRONMENTS").split(",")
__environments = {e: {"jenkins_uri": os.getenv("ENVIRONMENT_{}_jenkins_uri".format(e).replace("-", "_"))} for e in __environment_list}

__pipelines_list = os.getenv("PIPELINES").split(",")
__pipelines = {p: os.getenv("PIPELINE_{}".format(p).replace("-", "_")).split(",") for p in __pipelines_list}

__releases_uri = os.getenv("RELEASES_URI")

PIPELINES = __pipelines
RELEASES_URI = __releases_uri
ENVIRONMENTS = __environments
