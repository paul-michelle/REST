from django.urls import path
from street_food_app.views import (
    TicketsListOrCreate,
    TicketsGetUpdateDelete
)

urlpatterns = [
    path('tickets/', TicketsListOrCreate.as_view()),
    path('tickets/<int:pk>', TicketsGetUpdateDelete.as_view()),
]
