from django.contrib.admin import (
    ModelAdmin,
    register,
)
from .models import (
    Ticket,
)


@register(Ticket)
class TicketModelAdmin(ModelAdmin):
    list_display = [field.name for field in Ticket._meta.get_fields()]
