from street_food_app.models import (
    Ticket,
    Developer,
)
from rest_framework import serializers
from rest_framework_mongoengine.serializers import DocumentSerializer
from .validators import valid_points_count

SPRINT_POINTS_CEILING = 10


class DeveloperSerializer(DocumentSerializer):
    """Developer Details"""

    class Meta:
        model = Developer
        fields = ['first_name', 'github_account', 'stack', 'hobbies']


class TaskSerializer(serializers.ModelSerializer):
    points = serializers.IntegerField(validators=[valid_points_count])

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


class TicketSerializer(TaskSerializer):
    """Ticket Details"""

    assigned_to = DeveloperSerializer()

    class Meta:
        model = Ticket
        fields = ['title', 'description', 'points', 'assigned_to']
