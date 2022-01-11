from street_food_app.models import (
    Ticket,
    Developer,
)
from rest_framework import serializers
from rest_framework_mongoengine.serializers import DocumentSerializer


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'


class DeveloperSerializer(DocumentSerializer):
    class Meta:
        model = Developer
        depth = 1
