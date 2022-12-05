from mongoengine import Document, StringField, DateTimeField, ListField, EmbeddedDocumentField, EmbeddedDocument
from datetime import datetime
from mongoengine import connect


connect(db='mydata', host='localhost', port=27017)


class Contact(Document):
    name = StringField(required=True, unique=True)
    email = StringField(required=True, unique=True)
    birthday = DateTimeField()
    phone = StringField(max_length=20, unique=True)
    address = StringField(max_length=70)


class Tag(EmbeddedDocument):
    name = StringField()


class Note(Document):
    title = StringField(required=True, unique=True)
    created = DateTimeField(default=datetime.now())
    text = StringField(max_length=800, required=True)
    tags = ListField(EmbeddedDocumentField(Tag))
