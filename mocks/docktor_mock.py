#!/usr/bin/env python

import cyclone.web
import sys
import json
import random
import semver

from twisted.internet import reactor
from twisted.python import log

apps = {
    "app-1": {
        "state_info": "Healthchecks completed OK", 
        "healthcheck": {
            "retries": 50, 
            "startup_retries": 50, 
            "endpoint": "/ping/ping", 
            "strict": True
        }, 
        "app": "app-1", 
        "attempt_count": 0, 
        "instances": 2, 
        "state": "deploying", 
        "noop": False, 
        "ver": "0.5.0", 
        "slots": 4, 
        "state_changed_at": 1443178248
    }, 
    "app-2": {
        "state_info": "Healthchecks completed OK", 
        "healthcheck": {
            "retries": 50, 
            "endpoint": "/ping/ping", 
            "startup_retries": 50, 
            "strict": True
        }, 
        "app": "app-2", 
        "attempt_count": 0, 
        "instances": 2, 
        "state": "healthy", 
        "noop": False, 
        "slots": 4, 
        "ver": "1.0.1", 
        "state_changed_at": 1443176079
    }, 
    "app-3": {
        "state_info": "Healthchecks completed OK", 
        "healthcheck": {
            "retries": 50, 
            "startup_retries": 50, 
            "endpoint": "/ping/ping", 
            "strict": True
        }, 
        "app": "app-3", 
        "attempt_count": 0, 
        "instances": 2, 
        "state": "unhealthy", 
        "noop": False, 
        "slots": 4, 
        "ver": "0.2.0", 
        "state_changed_at": 1443044767
    }, 
    "app-4": {
        "state_info": "Healthchecks completed OK", 
        "healthcheck": {
            "strict": True, 
            "endpoint": "/ping/ping", 
            "startup_retries": 50, 
            "retries": 50
        }, 
        "app": "app-4", 
        "attempt_count": 0, 
        "instances": 2, 
        "state": "healthy", 
        "noop": False, 
        "slots": 4, 
        "ver": "0.7.0", 
        "state_changed_at": 1443113115
    }, 
    "app-5": {
        "state_info": "Healthchecks completed OK", 
        "healthcheck": {
            "strict": True, 
            "endpoint": "/ping/ping", 
            "startup_retries": 50, 
            "retries": 50
        }, 
        "app": "app-5", 
        "attempt_count": 0, 
        "instances": 2, 
        "state": "healthy", 
        "noop": False, 
        "slots": 4, 
        "ver": "2.3.0", 
        "state_changed_at": 1443176042
    }
}

class AppsHandler(cyclone.web.RequestHandler):
    def initialize(self, apps):
        self.apps = apps
    def get(self):
        self.write(json.dumps(self.apps.keys()))

class AppHandler(cyclone.web.RequestHandler):
    # def initialize(self, apps, prev_apps):
    def initialize(self, apps):
        self.apps = apps
        # self.prev_apps = prev_apps
    def get(self, app):
        try:
            app_details = {k: v for k, v in self.apps[app].items() if k != "ver"}
            app_details["slug_uri"] = "https://slughost/slugs/{app}/{app}_{ver}.tgz".format(app=app, ver=self.apps[app]["ver"])
            self.write(json.dumps(app_details))
        except KeyError:
            self.set_status(404)
            self.finish()
    def patch(self, app):
        print "patched {}".format(app)
        request = json.loads(self.request.body)
        if app not in self.apps:
            self.set_status(404)
            self.finish()
            return
        ver = request["slug_uri"].split("_")[1].rstrip(".tgz")
        self.apps[app]["ver"] = ver
        self.apps[app]["state"] = "deploying"
        reactor.callLater(random.randint(0,10), self.apps[app].__setitem__, "state", random.choice(["healthy", "unhealthy"]))

if __name__ == "__main__":
    try:
        port = int(sys.argv[1])
    except IndexError:
        port = 8888
    for stage_num in xrange(0,2):
        stage_port = port + stage_num
        application = cyclone.web.Application([
            (r"/apps/", AppsHandler, dict(apps={k: v for k, v in apps.items()})),
            (r"/apps/(.*)", AppHandler, dict(apps={k: dict(v.items() + {"ver": semver.bump_minor(v["ver"]) if stage_num > 0 else v["ver"]}.items()) for k, v in apps.items()}))
        ])

        log.startLogging(sys.stdout)
        reactor.listenTCP(stage_port, application)
    reactor.run()
