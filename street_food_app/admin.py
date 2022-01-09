from django.contrib import admin
from .models import Ticket


@admin.register(Ticket)
class TicketModelAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Ticket._meta.get_fields()]
