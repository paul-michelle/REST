import sys

from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task
def log_me():
    sys.stdout.write('Can you see me?')
    logger.info("Provided you've properly set up this shared task via celery beat, "
                "you are now reading it... I will pop up again in a minute!")
