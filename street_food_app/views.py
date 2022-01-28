import rest_framework.response
import rest_framework.request
from rest_framework import status
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from django.db import transaction
from drf_spectacular.utils import extend_schema
from street_food_app.serializers import TicketSerializer
from .views_utils import (
    upsert_ticket,
    get_all_tickets,
    delete_ticket,
    get_ticket,
)


class TicketsListOrCreate(ListCreateAPIView):
    def get_serializer_class(self):
        return TicketSerializer

    def get_queryset(self):
        pass

    @extend_schema(responses=TicketSerializer)
    @transaction.atomic
    def get(self, request, *args, **kwargs):
        data = get_all_tickets()
        return rest_framework.response.Response(data=data, status=status.HTTP_200_OK)

    @extend_schema(request=TicketSerializer, responses={201: TicketSerializer})
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        ticket_data, errors = upsert_ticket(request)
        if errors:
            return rest_framework.response.Response(data=errors, status=status.HTTP_400_BAD_REQUEST)
        return rest_framework.response.Response(data=ticket_data, status=status.HTTP_201_CREATED)


class TicketsGetUpdateDelete(RetrieveUpdateDestroyAPIView):
    def get_serializer_class(self):
        return TicketSerializer

    def get_queryset(self):
        pass

    @extend_schema(responses={200: TicketSerializer})
    @transaction.atomic
    def get(self, request, *args, **kwargs):
        successfully_found, ticket_data = get_ticket(kwargs['pk'])
        if successfully_found:
            return rest_framework.response.Response(data=ticket_data, status=status.HTTP_200_OK)
        return rest_framework.response.Response(status=status.HTTP_404_NOT_FOUND)

    @extend_schema(request=TicketSerializer)
    @transaction.atomic
    def put(self, request, *args, **kwargs):
        results = upsert_ticket(request, kwargs['pk'])
        if not results:
            return rest_framework.response.Response(status=status.HTTP_404_NOT_FOUND)
        ticket_data, errors = results
        if errors:
            return rest_framework.response.Response(data=errors, status=status.HTTP_400_BAD_REQUEST)
        return rest_framework.response.Response(status=status.HTTP_200_OK)

    @extend_schema(responses=TicketSerializer)
    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        successfully_deleted = delete_ticket(kwargs['pk'])
        if successfully_deleted:
            return rest_framework.response.Response(status=status.HTTP_204_NO_CONTENT)
        return rest_framework.response.Response(status=status.HTTP_404_NOT_FOUND)

    @extend_schema(exclude=True)
    def patch(self, request, *args, **kwargs):
        return rest_framework.response.Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
