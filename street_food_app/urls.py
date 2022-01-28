from django.urls import path
from street_food_app.views import (
    TicketsListOrCreate,
    TicketsGetUpdateDelete
)

urlpatterns = [
    path('tickets/', TicketsListOrCreate.as_view(), name='tickets_list_or_create_one'),
    path('tickets/<int:pk>', TicketsGetUpdateDelete.as_view(), name='tickets_get_update_delete_one')
]
