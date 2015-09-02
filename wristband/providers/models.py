from datetime import datetime

from mongoengine import Document, StringField, ComplexDateTimeField, ReferenceField, IntField, QuerySet

from wristband.apps.models import App


class TimeSortedQuerySet(QuerySet):
    def ordered_by_time(self, desc=True):
        return sorted(self.fields(), key=lambda x: x.start_time, reverse=desc)


class Job(Document):
    app = ReferenceField(App)
    provider_name = StringField(max_length=200)
    provider_id = IntField()
    start_time = ComplexDateTimeField(default=datetime.now())

    meta = {'queryset_class': TimeSortedQuerySet}

    def __str__(self):
        return '{name} job number {number} started at {time}'.format(
            name=self.provider_name,
            number=self.provider_id,
            time=self.start_time
        )
