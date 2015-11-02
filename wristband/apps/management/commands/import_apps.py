from django.core.management.base import BaseCommand
from wristband.apps.models import App
from wristband.apps.providers import NestedDocktorAppDataProvider


class Command(BaseCommand):
    help = 'Maps the apps to the relevant security zones'

    def handle(self, *args, **options):
        ndadp = NestedDocktorAppDataProvider()
        for app in ndadp.to_models():
            if not App.objects(name=app['name']).first():
                App(**{k: v for k, v in app.items() if k != "stage"}).save()
