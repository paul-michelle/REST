from django.urls import path
from street_food_app.views import ticket_list_or_create_next

urlpatterns = [
    path('tickets/', ticket_list_or_create_next),
]
