from street_food_app.models import (
    Ticket,
    Developer,
)
from rest_framework import serializers
from rest_framework_mongoengine.serializers import DocumentSerializer

SPRINT_POINTS_CEILING = 10


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'created', 'title', 'description', 'points']

    def validate(self, attrs) -> None:
        points: int
        points = 0
        for ticket in Ticket.objects.all():
            points += ticket.points
            if points >= SPRINT_POINTS_CEILING:
                raise serializers.ValidationError('Points upper limit for the current sprint reached')
        return attrs


class DeveloperSerializer(DocumentSerializer):
    class Meta:
        model = Developer
        fields = ['first_name', 'github_account', 'stack', 'hobbies']
        depth = 1
