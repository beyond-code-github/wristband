from mongoengine import Document, StringField

class App(Document):
    name = StringField(max_length=50)
    security_zone = StringField(max_length=50)

