import rest_framework.response
import rest_framework.request
from mongoengine.errors import DoesNotExist
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
def ticket_list_or_create_next(request: HttpRequest) -> rest_framework.response.Response:
    request: rest_framework.request.Request

    if request.method == 'GET':
        data = []
        tickets = Ticket.objects.all()
        for ticket in tickets:
            serializer_sql = TicketSerializer(ticket)
            developer_info = Developer.objects.get(github_account=ticket.assigned_to)
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
