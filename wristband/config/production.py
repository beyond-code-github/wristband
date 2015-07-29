# config.py

import os
import re

from utils import Environment

_environments = [Environment.from_environment_name(env_name) for env_name in os.getenv("ENVIRONMENTS").split(",")]

for env in _environments:
    jenkins_uri = os.getenv("ENVIRONMENT_{env}_jenkins_uri".format(env=env.name).replace("-", "_"))
    if not re.match('https.*', jenkins_uri):
        print "WARNING: {} should be https".format(jenkins_uri)
    else:
        env.jenkins_uri = jenkins_uri

__pipelines_list = os.getenv("PIPELINES").split(",")
__pipelines = {p: os.getenv("PIPELINE_{}".format(p).replace("-", "_")).split(",") for p in __pipelines_list}

__releases_uri = os.getenv("RELEASES_URI")

PIPELINES = __pipelines
RELEASES_URI = __releases_uri
ENVIRONMENTS = _environments
