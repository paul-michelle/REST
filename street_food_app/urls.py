from django.urls import path
from street_food_app.views import (
    ticket_list_all_or_create_one,
    ticket_read_update_delete_one,
)

urlpatterns = [
    path('tickets/', ticket_list_all_or_create_one),
    path('tickets/<int:pk>', ticket_read_update_delete_one),
]
