# config.py

import os
import re

__environment_list = os.getenv("ENVIRONMENTS").split(",")
__environments = {}

for env in __environment_list:
    environment_jenkins = os.getenv("ENVIRONMENT_{}_jenkins_uri".format(env).replace("-", "_"))
    if not re.match('https.*', environment_jenkins):
        print "WARNING: {} should be https".format(environment_jenkins)
    else:
        __environments[env] = {"jenkins_uri": os.getenv("ENVIRONMENT_{}_jenkins_uri".format(env).replace("-", "_"))}

__pipelines_list = os.getenv("PIPELINES").split(",")
__pipelines = {p: os.getenv("PIPELINE_{}".format(p).replace("-", "_")).split(",") for p in __pipelines_list}

__releases_uri = os.getenv("RELEASES_URI")

PIPELINES = __pipelines
RELEASES_URI = __releases_uri
ENVIRONMENTS = __environments
