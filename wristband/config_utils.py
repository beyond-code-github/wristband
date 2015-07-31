import os


def environments_factory():
    environments = {}
    for env in os.getenv("ENVIRONMENTS").split(","):
        environment_jenkins = os.getenv(
            "ENVIRONMENT_{environment}_jenkins_uri".format(environment=env).replace("-", "_"))
        if environment_jenkins.startswith('https://'):
            environments[env] = {"jenkins_uri": environment_jenkins}
        else:
            print("WARNING {jenkins_url} should be https".format(jenkins_url=environment_jenkins))
    return environments


def pipelines_factory():
    return {pipeline: os.getenv("PIPELINE_{pipeline}".format(pipeline=pipeline).replace("-", "_")).split(",") for
            pipeline in os.getenv("PIPELINES").split(",")}
