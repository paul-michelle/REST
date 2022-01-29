import pytest
from .helpers import (
    write_random_n_tickets_and_pick_up_one_out_of_sent_tickets,
    retrieve_ticket_by_id,
    update_ticket,
    delete_ticket,
)


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_can_get_ticket_by_id(sample_ticket):
    ticket_sent, index_of_ticket_sent = write_random_n_tickets_and_pick_up_one_out_of_sent_tickets(sample_ticket)
    response = retrieve_ticket_by_id(index_of_ticket_sent + 1)
    assert response.status_code == 200

    ticket_received = response.data
    assert ticket_sent["assigned_to"] == ticket_received["assigned_to"]


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_can_write_tickets_pick_random_one_and_upd_it_with_valid_info(sample_ticket):
    ticket_sent, index_of_ticket_sent = write_random_n_tickets_and_pick_up_one_out_of_sent_tickets(sample_ticket)
    response = retrieve_ticket_by_id(index_of_ticket_sent + 1)
    assert response.status_code == 200

    ticket_received = response.data
    assert ticket_sent["title"] == ticket_received["title"]
    assert ticket_sent["points"] == ticket_received["points"]
    assert ticket_sent["assigned_to"] == ticket_received["assigned_to"]

    ticket_sent["title"] += "(UPD)"
    developer_assigned = ticket_sent["assigned_to"]
    developer_assigned["stack"].append(
        {
            "language_name": "Golang",
            "experience": .5,
            "description": "Basics"
        }
    )

    update_data = ticket_sent
    id_ = ticket_received["id"]
    response = update_ticket(id_, update_data)
    assert response.status_code == 200

    updated_ticket = response.data
    assert ticket_sent["title"] == updated_ticket["title"]
    assert ticket_sent["points"] == updated_ticket["points"]
    assert ticket_sent["assigned_to"] == updated_ticket["assigned_to"]

    non_fibonacci_sequence_integer = 4
    ticket_sent["points"] = non_fibonacci_sequence_integer
    update_data = ticket_sent
    id_ = ticket_received["id"]
    response = update_ticket(id_, update_data)
    assert response.status_code == 400


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_can_write_tickets_pick_random_one_and_delete_it(sample_ticket):
    ticket_sent, index_of_ticket_sent = write_random_n_tickets_and_pick_up_one_out_of_sent_tickets(sample_ticket)
    response = retrieve_ticket_by_id(index_of_ticket_sent + 1)
    assert response.status_code == 200

    ticket_received = response.data
    id_ = ticket_received["id"]
    response = delete_ticket(id_)
    assert response.status_code == 204

    response = retrieve_ticket_by_id(id_)
    assert response.status_code == 404
