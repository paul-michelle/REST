import random
import pytest
from .helpers import (
    write_one_ticket,
    make_up_numerous_unique_tickets,
    get_all_written_tickets,
    TICKETS_TO_SEND_COUNT
)
from street_food_app import pydantic_schemas
from collections import OrderedDict


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_ticket_is_written_successfully(sample_ticket):
    response = write_one_ticket(sample_ticket)
    assert response.status_code == 201
    assert response.data['assigned_to']['first_name'] == sample_ticket['assigned_to']['first_name']


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_fields_id_and_created_at_are_added_to_the_object(sample_ticket):
    response = write_one_ticket(sample_ticket)
    assert response.data.items() != OrderedDict(sample_ticket).items()
    added_keys = set(response.data) - set(OrderedDict(sample_ticket))
    assert added_keys == {'id', 'created'}

    response.data.pop('id')
    response.data.pop('created')
    assert response.data.items() == OrderedDict(sample_ticket).items()


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_a_number_of_unique_tickets_written_and_retrieved_one_by_one(sample_ticket):
    tickets_to_send = make_up_numerous_unique_tickets(TICKETS_TO_SEND_COUNT, sample_ticket)
    tickets_written = [write_one_ticket(ticket).data for ticket in tickets_to_send]
    developers_written = [ticket["assigned_to"] for ticket in tickets_written]

    assert len(tickets_written) == TICKETS_TO_SEND_COUNT
    assert len(developers_written) == TICKETS_TO_SEND_COUNT

    unique_github_links = set(developer["github_account"] for developer in developers_written)
    developers_are_unique: bool = len(unique_github_links) == TICKETS_TO_SEND_COUNT
    assert developers_are_unique is True


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_a_number_of_unique_tickets_written_and_list_of_all_tickets_retrieved(sample_ticket):
    tickets_to_send = make_up_numerous_unique_tickets(TICKETS_TO_SEND_COUNT, sample_ticket)
    for ticket in tickets_to_send:
        write_one_ticket(ticket)
    response = get_all_written_tickets()
    assert response.status_code == 200
    assert len(response.data) == TICKETS_TO_SEND_COUNT

    random_ticket_out_of_response = random.choice(response.data)
    ticket_filtered = pydantic_schemas.TicketInfoInResponse(**random_ticket_out_of_response)
    assert dict(ticket_filtered).keys() == random_ticket_out_of_response.keys()
