from datetime import datetime
import binascii
import os

from mongoengine import Document, StringField, DateTimeField, ReferenceField
from mongoengine.django.mongo_auth.models import get_user_document

AUTH_USER_MODEL = get_user_document()


class Token(Document):
    key = StringField(max_length=40, primary_key=True)
    user = ReferenceField(AUTH_USER_MODEL)
    created = DateTimeField(default=datetime.now())

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(Token, self).save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key
