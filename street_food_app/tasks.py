import sys
from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.mail import send_mail
from street_food_app.models import Ticket

logger = get_task_logger(__name__)


@shared_task
def log_me():
    sys.stdout.write('Can you see me?')
    logger.info("Provided you've properly set up this shared task via celery beat, "
                "you are now reading it... I will pop up again in a minute!")


@shared_task()
def send_mail_with_tickets_count():
    send_mail(
        'Your tickets',
        f'Number of tickets created so far: {Ticket.objects.count()}',
        'from@example.com',
        ['streetfoodincentive@gmail.com'],
        fail_silently=False,
    )
