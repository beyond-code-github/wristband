from wristband.apps.models import App
from wristband.providers.models import Job
from wristband.providers.service_providers import JenkinsServiceProvider

PROVIDERS_LOOKUP = {
    'jenkins': JenkinsServiceProvider
}


def extract_stage(environment):
    return environment.split('-')[0]


def extract_security_zone_from_env(environment):
    try:
        return environment.split('-')[1]
    except IndexError:
        return environment


def get_security_zone_from_app_name(app_name):
    app = App.objects(name=app_name).first()
    security_zone = app.security_zone if app else None
    return security_zone


def get_last_job_id_by_app_name(app_name, stage):
    # FIXME, investigate __ to avoid doing two queries
    app = App.objects.get(name=app_name, stage=stage)
    return str(Job.objects(app=app).ordered_by_time(desc=True)[0].id)


def get_last_job_status_by_app_name(app_name, stage):
    job_id = get_last_job_id_by_app_name(app_name, stage)
    job = Job.objects.get(id=job_id)
    print job.provider_id
    return get_last_job_status_by_job(job)


def get_last_job_status_by_job(job):
    return PROVIDERS_LOOKUP[job.provider_name](job.app.name, job.app.stage).status(job)
