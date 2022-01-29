import copy
import random
from typing import List, Tuple
from street_food_app.datatypes import TicketInfo
from street_food_app.views import (
    TicketsListOrCreate,
    TicketsGetUpdateDelete
)
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory

request_factory = APIRequestFactory()
TICKETS_TO_SEND_COUNT = 10


def write_one_ticket(data: TicketInfo) -> Response:
    post_request = request_factory.post(
        path=reverse(viewname='tickets_list_or_create_one'),
        data=data,
        format='json'
    )
    return TicketsListOrCreate.as_view()(post_request)


def get_all_written_tickets() -> Response:
    get_request = request_factory.get(
        path=reverse(viewname='tickets_list_or_create_one'),
    )
    return TicketsListOrCreate.as_view()(get_request)


def retrieve_ticket_by_id(id_: int) -> Response:
    get_request = request_factory.get(
        path=reverse(
            viewname='tickets_get_update_delete_one',
            kwargs={"pk": id_}
        )
    )
    return TicketsGetUpdateDelete.as_view()(get_request, pk=id_)


def make_up_numerous_unique_tickets(count: int, roll_back_transaction: TicketInfo) -> List[TicketInfo]:
    tickets_to_send = []
    for i in range(count):
        new_ticket = copy.deepcopy(roll_back_transaction)
        new_ticket["assigned_to"]["github_account"] += f"{i}"
        tickets_to_send.append(new_ticket)
    return tickets_to_send


def write_random_n_tickets_and_pick_up_one_out_of_sent_tickets(sample_ticket: TicketInfo) -> Tuple[TicketInfo, int]:
    tickets_to_send_random_count = random.randint(1, TICKETS_TO_SEND_COUNT)
    tickets_to_send = make_up_numerous_unique_tickets(tickets_to_send_random_count, sample_ticket)
    for ticket in tickets_to_send:
        write_one_ticket(ticket)

    pseudo_randomly_chosen_index = random.randint(0, tickets_to_send_random_count - 1)
    one_of_tickets_sent = tickets_to_send[pseudo_randomly_chosen_index]
    return one_of_tickets_sent, pseudo_randomly_chosen_index
