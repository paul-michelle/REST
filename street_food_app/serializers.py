from street_food_app.models import (
    Ticket,
    Developer,
)
from rest_framework import serializers
from rest_framework_mongoengine.serializers import DocumentSerializer

SPRINT_POINTS_CEILING = 10


class TicketSerializer(serializers.ModelSerializer):

    def validate(self, attrs) -> None:
        points: int
        points = 0
        for ticket in Ticket.objects.all():
            points += ticket.points
            if points >= SPRINT_POINTS_CEILING:
                raise serializers.ValidationError('Points upper limit for the current sprint reached')
        return attrs

    class Meta:
        model = Ticket
        fields = '__all__'


class DeveloperSerializer(DocumentSerializer):
    class Meta:
        model = Developer
        depth = 1
