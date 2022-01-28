from typing import List

import pytest
import copy
from street_food_app.datatypes import TicketInfo
from collections import OrderedDict
from street_food_app.views import (
    TicketsListOrCreate,
    TicketsGetUpdateDelete
)
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory

request_factory = APIRequestFactory()


def write_one_ticket(data: TicketInfo) -> Response:
    post_request = request_factory.post(
        path=reverse(viewname='tickets_list_or_create_one'),
        data=data,
        format='json'
    )
    response = TicketsListOrCreate.as_view()(post_request)
    return response


def make_up_numerous_unique_tickets(count: int, sample_ticket: TicketInfo) -> List[TicketInfo]:
    tickets_to_send = []
    for i in range(count):
        new_ticket = copy.deepcopy(sample_ticket)
        new_ticket["assigned_to"]["github_account"] += f"{i}"
        tickets_to_send.append(new_ticket)
    return tickets_to_send


@pytest.mark.django_db
def test_ticket_is_written_successfully(generate_sample_ticket):
    response = write_one_ticket(generate_sample_ticket)
    assert response.status_code == 201
    assert response.data['assigned_to']['first_name'] == generate_sample_ticket['assigned_to']['first_name']


@pytest.mark.django_db
def test_id_and_created_at_fields_added(generate_sample_ticket):
    response = write_one_ticket(generate_sample_ticket)
    assert response.data.items() != OrderedDict(generate_sample_ticket).items()
    added_keys = set(response.data) - set(OrderedDict(generate_sample_ticket))
    assert added_keys == {'id', 'created'}

    response.data.pop('id')
    response.data.pop('created')
    assert response.data.items() == OrderedDict(generate_sample_ticket).items()


@pytest.mark.django_db
def test_a_number_of_unique_tickets_written_and_retrieved_one_by_one(generate_sample_ticket):
    tickets_to_send_count = 10
    tickets_to_send = make_up_numerous_unique_tickets(tickets_to_send_count, generate_sample_ticket)
    tickets_written = [write_one_ticket(ticket).data for ticket in tickets_to_send]
    developers_written = [ticket["assigned_to"] for ticket in tickets_written]

    assert len(tickets_written) == tickets_to_send_count
    assert len(developers_written) == tickets_to_send_count

    unique_github_links = set(developer["github_account"] for developer in developers_written)
    developers_are_unique: bool = len(unique_github_links) == tickets_to_send_count
    assert developers_are_unique is True


@pytest.mark.skip
@pytest.mark.django_db
def test_a_number_of_unique_tickets_written_and_list_of_tickets_retrieved(generate_sample_ticket):
    pass
