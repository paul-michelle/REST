import rest_framework.response
import rest_framework.request
from mongoengine.errors import DoesNotExist
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest
from rest_framework import status
from rest_framework.decorators import api_view
from street_food_app.serializers import (
    TicketSerializer,
    DeveloperSerializer,
)
from street_food_app.models import (
    Ticket,
    Developer,
)


@api_view(['GET', 'POST'])
def ticket_list_all_or_create_one(request: HttpRequest) -> rest_framework.response.Response:
    request: rest_framework.request.Request

    if request.method == 'GET':
        data = []
        there_are_tickets = Ticket.objects.count()
        if there_are_tickets:
            for ticket in Ticket.objects.all():
                serializer_sql = TicketSerializer(ticket)
                try:
                    developer_info = Developer.objects.get(github_account=ticket.assigned_to)
                except DoesNotExist:
                    break
                serializer_nosql = DeveloperSerializer(developer_info)
                data.extend([serializer_sql.data, serializer_nosql.data])
        return rest_framework.response.Response(data)

    if request.method == 'POST':
        developer_info = request.data.pop('developer')
        serializer_sql = TicketSerializer(data=request.data)
        serializer_nosql = DeveloperSerializer(data=developer_info)

        serializer_sql.is_valid()
        serializer_nosql.is_valid()

        if serializer_sql.is_valid() and serializer_nosql.is_valid():
            serializer_sql.save()
            try:
                Developer.objects.get(github_account=developer_info['github_account'])
            except DoesNotExist:
                serializer_nosql.save()
            data = [serializer_sql.data, serializer_nosql.data]
            return rest_framework.response.Response(data=data, status=status.HTTP_201_CREATED)

        errors = [serializer_sql.errors, serializer_nosql.errors]
        return rest_framework.response.Response(data=errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def ticket_read_update_delete_one(request: HttpRequest, pk: int) -> rest_framework.response.Response:
    request: rest_framework.request.Request
    try:
        ticket_requested = Ticket.objects.get(id=pk)
    except ObjectDoesNotExist:
        return rest_framework.response.Response(status=status.HTTP_404_NOT_FOUND)
    developer_github = ticket_requested.assigned_to
    developer_requested = Developer.objects.get(github_account=developer_github)

    if request.method == 'DELETE':
        developer_requested_has_no_other_tickets = not (Ticket.objects.filter(assigned_to=developer_github).count() - 1)
        if developer_requested_has_no_other_tickets:
            developer_requested.delete()
        ticket_requested.delete()
        return rest_framework.response.Response(status=status.HTTP_204_NO_CONTENT)

    if request.method == 'GET':
        serialized_ticket = TicketSerializer(ticket_requested)
        serialized_developer = DeveloperSerializer(developer_requested)
        data = serialized_ticket.data
        data.update(serialized_developer.data)
        return rest_framework.response.Response(data=data, status=status.HTTP_200_OK)

    if request.method == 'PUT':
        return rest_framework.response.Response(status=status.HTTP_204_NO_CONTENT)

    return rest_framework.response.Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
