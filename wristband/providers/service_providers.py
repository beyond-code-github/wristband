from time import sleep
import logging

import jenkins

from . import providers_config
from .generics import ServiceProvider
from wristband.providers.exceptions import DeployException
from wristband.apps.models import App
from wristband.providers.models import Job

JENKINS_CALL_SAFE_LIMIT = 8

logger = logging.getLogger('wristband.provider')


class JenkinsServiceProvider(ServiceProvider):
    def __init__(self, app_name, stage):
        self.app = App.objects.get(name=app_name, stage=stage)
        config = self.get_jenkins_server_config()
        self.server = jenkins.Jenkins(config['uri'],
                                      username=config['username'],
                                      password=config['password'])
        self.job_name = config['job_name']

    def get_jenkins_server_config(self):
        return providers_config.providers['jenkins'][self.app.stage][self.app.security_zone]

    def deploy(self, version):
        params = {
            "APP": self.app.name,
            "APP_BUILD_NUMBER": version
        }
        try:
            self.server.build_job(self.job_name, parameters=params)
        except jenkins.JenkinsException as e:
            raise DeployException(e.message)
        return self.save_job_info(version)

    def save_job_info(self, version):
        potential_build_id = self.server.get_job_info(self.job_name)['nextBuildNumber']
        count = 0
        job = None
        while count <= JENKINS_CALL_SAFE_LIMIT:
            try:
                # Jenkins API don't return the job id when a job is posted, it's a known bug.
                # https://issues.jenkins-ci.org/browse/JENKINS-26228
                # This is because the job is queued first and the job id doesn't become available until the
                # grace period is over. The following solution is a bit nasty but it's the only approach I could think
                # about until Jenkins solve the bug.
                # We get the next build number straight after starting the job, then keep asking jenkins api for that
                # particular job number info. Jenkins will return 404 until the job has actually started.
                # We then check that the version associate to the job number is what we are expecting it to be
                # If not, we're screwed. Although this feels quite safe, job number clashing will occur only when two
                # users click the deploy button exactly at the same time.
                build_info = self.server.get_build_info(self.job_name, potential_build_id)
                version_param_dictionary = \
                    filter(lambda x: x['name'] == 'APP_BUILD_NUMBER', build_info['actions'][0]['parameters'])[0]
                version_to_check = version_param_dictionary['value']
                if version_to_check == version:
                    job = Job(app=self.app, provider_name='jenkins', provider_id=potential_build_id)
                    job.save()
                    logger.info('Job started for {app} with job ID {job_id}'.format(app=self.app.name, job_id=job.id))
            except jenkins.NotFoundException:
                sleep(1)  # prevents from bashing Jenkins too often
                count += 1
            if not job:
                logger.warning('Job for {app} not started on Jenkins'.format(app=self.app.name))
            return job.id if job else None

    def status(self, job):
        build_info = self.server.get_build_info(self.job_name, job.provider_id)
        return build_info['building'] or build_info['result']
