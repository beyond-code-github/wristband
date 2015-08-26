from datetime import datetime

from mongoengine import Document, StringField, ComplexDateTimeField, ReferenceField, IntField

from wristband.apps.models import App


class Job(Document):
    app = ReferenceField(App)
    provider_name = StringField(max_length=200)
    provider_id = IntField()
    start_time = ComplexDateTimeField(default=datetime.now())

    meta = {
        'ordering': ['-start_time']
    }

