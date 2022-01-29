import pytest
from .helpers import (
    retrieve_ticket_by_id,
    write_random_n_tickets_and_pick_up_one_out_of_sent_tickets,

)


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_can_get_ticket_by_id(sample_ticket):
    ticket_sent, index_of_ticket_sent = write_random_n_tickets_and_pick_up_one_out_of_sent_tickets(sample_ticket)
    response = retrieve_ticket_by_id(index_of_ticket_sent + 1)
    assert response.status_code == 200

    ticket_received = response.data
    assert ticket_sent["assigned_to"] == ticket_received["assigned_to"]


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_can_write_one_ticket_and_then_upd_it(sample_ticket):
    ticket_sent, index_of_ticket_sent = write_random_n_tickets_and_pick_up_one_out_of_sent_tickets(sample_ticket)
    response = retrieve_ticket_by_id(index_of_ticket_sent + 1)
    assert response.status_code == 200

    ticket_received = response.data
    ticket_received_id = ticket_received["id"]

    upd_data = ...
