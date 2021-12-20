from django.db import models

DEFAULT_TICKET_TITLE = 'Ticket'
DEFAULT_TICKET_DESCRIPTION = 'Another BE ticket'


class Ticket(models.Model):
    """Test model."""

    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=55, default=DEFAULT_TICKET_TITLE)
    description = models.TextField(default=DEFAULT_TICKET_DESCRIPTION)
    points = models.IntegerField(default=1)
    objects = models.Manager()

    class Meta:
        ordering = ['created', ]
