"""
This module stores models to store contacts and notes in the database.
"""

from datetime import datetime

from mongoengine import (
    Document,
    StringField,
    DateTimeField,
    ListField,
    EmbeddedDocumentField,
    EmbeddedDocument,
    connect,
)

connect(db="mydata", host="localhost", port=27017)


class Contact(Document):
    """
    Represents a contact.
    """

    name = StringField(required=True, unique=True)
    email = StringField(required=True, unique=True)
    birthday = DateTimeField()
    phone = StringField(max_length=20, unique=True)
    address = StringField(max_length=70)


class Tag(EmbeddedDocument):
    """
    Represents a tag.
    """

    name = StringField()


class Note(Document):
    """
    Represents a note.
    """

    title = StringField(required=True, unique=True)
    created = DateTimeField(default=datetime.now())
    text = StringField(max_length=800, required=True)
    tags = ListField(EmbeddedDocumentField(Tag))
