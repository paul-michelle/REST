from django.core.management.base import BaseCommand
from django.db import transaction
from mongoengine.errors import OperationError
from psycopg2 import OperationalError
from street_food_app.models import (
    Developer,
    Ticket
)


class Command(BaseCommand):
    help = 'Removes all data on Tickets BOTH from PostgreSQL and MongoDB databases'

    def _get_tickets_count(self):
        try:
            return Ticket.objects.count()
        except (ConnectionError, OperationalError) as e:
            self.stdout.write(
                self.style.ERROR(
                    f'Error when retrieving tickets\'s count from PostgreSQL db occurred: {e}'
                )
            )
            raise

    def _get_developers_count(self):
        try:
            return Developer.objects.count()
        except (ConnectionError, OperationError) as e:
            self.stdout.write(
                self.style.ERROR(
                    f'Error when retrieving developers\'s count from MongoDB db occurred: {e}'
                )
            )
            raise

    @staticmethod
    def _remove_info_on_tickets():
        Ticket.objects.all().delete()

    @staticmethod
    def _remove_docs_on_developers():
        Developer.objects.all().delete()

    @transaction.atomic
    def _flush(self):
        self._remove_docs_on_developers()
        self._remove_info_on_tickets()

    def handle(self, *args, **options):
        message = f'Successfully deleted info on {self._get_developers_count()} ticket(s) from MongoDB ' \
                  f'and {self._get_tickets_count()} ticket(s) from PostgreSQL'
        try:
            self._flush()
        except (ConnectionError, OperationError, OperationalError) as e:
            raise RuntimeError(f'Error when deleting info occurred: {e}') from e

        self.stdout.write(
            self.style.SUCCESS(message)
        )
