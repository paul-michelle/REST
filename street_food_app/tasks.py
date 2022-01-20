import json
import sys
from typing import List, Dict, Any
from dataclasses import asdict
from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.mail import send_mail
from mongoengine.errors import DoesNotExist

from street_food_app.datatypes import (
    ExpertiseInfo,
    DeveloperInfo,
    TicketInfo,
)

from street_food_app.models import (
    Ticket,
    Developer,
)

logger = get_task_logger(__name__)


def get_info_on_latest_tickets(count) -> List[Dict[str, Any]]:
    info: List[json]
    info = list()

    if Ticket.objects.count():
        for ticket in Ticket.objects.all().order_by('-id')[:count]:
            try:
                developer_obj = Developer.objects.get(github_account=ticket.assigned_to)
            except DoesNotExist:
                break
            stack_objs = developer_obj.stack
            stack_info = [
                ExpertiseInfo(stack_obj.language_name, stack_obj.experience, stack_obj.description)
                for stack_obj in stack_objs
            ]
            developer_info = DeveloperInfo(developer_obj.first_name, developer_obj.github_account, stack_info)
            single_ticket_info = asdict(
                TicketInfo(
                    ticket.created,
                    ticket.title,
                    ticket.description,
                    ticket.points,
                    developer_info
                )
            )

            info.append(json.dumps(single_ticket_info, indent=4))

    return info


@shared_task
def log_tickets_total() -> None:
    sys.stdout.write('Logging is following...')
    logger.info(f"Number of registered tickers so far is: {Ticket.objects.count()}")


@shared_task()
def send_mail_on_latest_tickets(count) -> None:
    send_mail(
        'Your tickets',
        str(get_info_on_latest_tickets(count)),
        'from@example.com',
        ['lieber.paul.git@gmail.com'],
        fail_silently=False,
    )
