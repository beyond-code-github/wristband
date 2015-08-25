from django.core.management.base import BaseCommand
from wristband.apps.models import App
from wristband.apps.providers import NestedReleaseAppDataProvider


class Command(BaseCommand):
    help = 'Maps the apps to the relevant security zones'

    def handle(self, *args, **options):
        for app in NestedReleaseAppDataProvider().to_models():
            if not App.objects(name=app['name']):
                App(**app).save()
