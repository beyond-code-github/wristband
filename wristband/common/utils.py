from wristband.apps.models import App


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
