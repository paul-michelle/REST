import rest_framework.response
import rest_framework.request
from django.http import HttpRequest
from rest_framework import status
from rest_framework.decorators import api_view
from street_food_app.serializers import TicketSerializer
from street_food_app.models import Ticket


@api_view(['GET', 'POST'])
def ticket_list_or_create_next(request: HttpRequest) -> rest_framework.response.Response:
    request: rest_framework.request.Request

    if request.method == 'GET':
        tickets = Ticket.objects.all()
        serializer = TicketSerializer(tickets, many=True)
        return rest_framework.response.Response(serializer.data)

    if request.method == 'POST':
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return rest_framework.response.Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return rest_framework.response.Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
