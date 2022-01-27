from django.db import models
from mongoengine import (
    Document,
    EmbeddedDocument
)
from mongoengine.fields import (
    EmbeddedDocumentListField,
    ListField,
    FloatField,
    StringField,
    URLField,
)

DEFAULT_TICKET_TITLE = 'Ticket'
DEFAULT_TICKET_DESCRIPTION = 'Another BE ticket'
DEFAULT_LANGUAGE = 'C++'
DEFAULT_GITHUB_ACCOUNT = 'https://github.com/whoami'


class Ticket(models.Model):
    """Test model."""

    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=55, default=DEFAULT_TICKET_TITLE)
    description = models.TextField(default=DEFAULT_TICKET_DESCRIPTION)
    points = models.IntegerField(default=1)
    assigned_to = models.URLField()

    objects = models.Manager()

    class Meta:
        ordering = ['created', ]


class Expertise(EmbeddedDocument):
    """Imitating an embedded document."""
    language_name = StringField(default=DEFAULT_LANGUAGE)
    experience = FloatField(default=1.5)
    description = StringField(default='')


class Developer(Document):
    """Imitating permanently changing data structure."""

    first_name = StringField(default='Whoami')
    github_account = URLField(default=DEFAULT_GITHUB_ACCOUNT)
    stack = EmbeddedDocumentListField(Expertise, default=[Expertise()])
    hobbies = ListField(default=['Art', 'Movies'])
