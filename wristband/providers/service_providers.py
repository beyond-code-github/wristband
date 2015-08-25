import jenkins

from . import providers_config

from .generics import ServiceProvider
from wristband.apps.models import App
from wristband.providers.models import Job


class JenkinsServiceProvider(ServiceProvider):
    def __init__(self, app_name):
        config = self.get_jenkins_server_config()

        self.server = jenkins.Jenkins(config['url'],
                                      username=config['username'],
                                      password=config['password'])
        self.app = App.objects(name=app_name).first()
        self.job_name = config['job_name']

    def get_jenkins_server_config(self):
        return providers_config.providers['jenkins'][self.app.stage][self.app.security_zone]

    def promote(self, version):
        params = {
            "APP": self.app.name,
            "APP_BUILD_NUMBER": version
        }
        self.server.build_job(self.job_name, parameters=params)
        self._save_job_info()

    def _save_job_info(self):
        build_id = self.server.get_job_info(self.job_name)['builds'][0]['number']
        job = Job(app=self.app, provider_name='jenkins', provider_id=build_id)
        job.save()

    def status(self, job_id):
        build_id = Job.objects(job_id).first().provider_id
        return self.server.get_build_info(self.job_name, build_id)['result']
