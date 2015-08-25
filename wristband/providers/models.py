from mongoengine import Document, StringField, DateTimeField, EmbeddedDocumentField

from wristband.apps.models import App


class Job(Document):
    app = EmbeddedDocumentField(App)
    provider_name = StringField(max_length=200)
    provider_id = StringField(max_length=200)
    job_started = DateTimeField()
