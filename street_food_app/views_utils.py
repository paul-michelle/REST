from mongoengine.errors import DoesNotExist
from django.core.exceptions import ObjectDoesNotExist

from street_food_app.datatypes import (
    TicketInfo,
    ErrorInfo
)

from street_food_app.serializers import (
    TaskSerializer,
    DeveloperSerializer
)

from street_food_app.models import (
    Ticket,
    Developer,
)

from typing import (
    Optional,
    List,
    Tuple,
)


def get_all_tickets() -> List[TicketInfo]:
    data = list()

    there_are_tickets = Ticket.objects.count()
    if there_are_tickets:
        for ticket in Ticket.objects.all():
            serializer_sql = TaskSerializer(ticket)
            try:
                developer_info = Developer.objects.get(github_account=ticket.assigned_to)
            except DoesNotExist:
                break
            serializer_nosql = DeveloperSerializer(developer_info)
            ticket_data = merge_data(serializer_sql, serializer_nosql)
            data.append(ticket_data)
    return data


def find_ticket_and_developer_in_question(pk) -> Tuple[bool, Ticket, Developer]:
    found = True
    ticket_requested = None
    developer_requested = None

    try:
        ticket_requested = Ticket.objects.get(id=pk)
    except ObjectDoesNotExist:
        found = False

    if found:
        developer_github = ticket_requested.assigned_to
        developer_requested = Developer.objects.get(github_account=developer_github)
    return found, ticket_requested, developer_requested


def merge_data(sql: TaskSerializer, nosql: DeveloperSerializer) -> TicketInfo:
    developer_data = {"assigned_to": nosql.data}
    ticket_data = sql.data
    ticket_data.update(developer_data)
    return ticket_data


def merge_errors(sql_errors: ErrorInfo,
                 nosql_errors: ErrorInfo) -> ErrorInfo:
    errors = sql_errors
    errors.update(nosql_errors)
    return errors


def delete_unassigned_developer(developer) -> None:
    developer_has_no_other_tickets = not (
            Ticket.objects.filter(assigned_to=developer['github_account']).count() - 1
    )
    if developer_has_no_other_tickets:
        developer.delete()


def upsert_ticket(request, pk: int = 0) -> Optional[Tuple[TicketInfo, ErrorInfo]]:
    ticket_data = None
    serializer_sql = None
    serializer_nosql = None
    developer_sent_info = request.data.pop('assigned_to')

    if pk:
        found, ticket_requested, developer_requested = find_ticket_and_developer_in_question(pk)
        if not found:
            return
        if developer_sent_info['github_account'] != developer_requested['github_account']:
            delete_unassigned_developer(developer_requested)
            serializer_nosql = DeveloperSerializer(data=developer_sent_info)
        if developer_sent_info['github_account'] == developer_requested['github_account']:
            serializer_nosql = DeveloperSerializer(data=developer_sent_info, instance=developer_requested)

        serializer_sql = TaskSerializer(data=request.data, instance=ticket_requested)

    if not pk:
        serializer_sql = TaskSerializer(data=request.data)
        serializer_nosql = DeveloperSerializer(data=developer_sent_info)

    serializer_sql.is_valid()
    serializer_nosql.is_valid()

    if serializer_sql.is_valid() and serializer_nosql.is_valid():
        serializer_sql.save(assigned_to=developer_sent_info['github_account'])
        if not pk:
            try:
                Developer.objects.get(github_account=developer_sent_info['github_account'])
            except DoesNotExist:
                serializer_nosql.save()
        if pk:
            serializer_nosql.save()
        ticket_data = merge_data(serializer_sql, serializer_nosql)

    errors = merge_errors(serializer_sql.errors, serializer_nosql.errors)
    return ticket_data, errors


def delete_ticket(pk: int) -> bool:
    success = False
    found, ticket_requested, developer_requested = find_ticket_and_developer_in_question(pk)
    if found:
        delete_unassigned_developer(developer_requested)
        ticket_requested.delete()
        success = True
    return success


def get_ticket(pk: int) -> Tuple[bool, TicketInfo]:
    success = False
    ticket_data = None
    found, ticket_requested, developer_requested = find_ticket_and_developer_in_question(pk)
    if found:
        serialized_ticket = TaskSerializer(ticket_requested)
        serialized_developer = DeveloperSerializer(developer_requested)
        ticket_data = merge_data(serialized_ticket, serialized_developer)
        success = True
    return success, ticket_data
