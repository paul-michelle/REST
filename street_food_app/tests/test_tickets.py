import pytest
from street_food_app.views import (
    TicketsListOrCreate,
    TicketsGetUpdateDelete
)
from django.urls import reverse
from rest_framework.test import APIRequestFactory

request_factory = APIRequestFactory()


@pytest.mark.django_db
def test_ticket_is_written_correctly(generate_ticket):
    post_request = request_factory.post(
        path=reverse(viewname='tickets_list_or_create_one'),
        data=generate_ticket,
        format='json'
    )
    response = TicketsListOrCreate.as_view()(post_request)
    print(response)
    assert response.status_code == 201
