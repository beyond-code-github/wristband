import re

from wristband.providers.service_providers import DocktorServiceProvider

PROVIDERS_LOOKUP = {
    'docktor': DocktorServiceProvider
}
VERSION_REGEX = r'\d+\.\d+\.\d+'


def extract_stage(environment):
    return environment.split('-')[0]


def extract_security_zone_from_env(environment):
    try:
        return environment.split('-')[1]
    except IndexError:
        return environment


def get_last_job_status_by_job(job):
    return PROVIDERS_LOOKUP[job.provider_name](job.app.name, job.app.stage).status(job)


def extract_version_from_slug(slug):
    try:
        version = re.findall(VERSION_REGEX, slug)[0]
    except IndexError:
        version = ''
    return version
