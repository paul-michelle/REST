import os
import celery
from datetime import timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "street_food_project.settings")

app = celery.Celery("street_food_project")
app.config_from_object("django.conf:settings", namespace='CELERY')

app.conf.beat_schedule = {
    "every_hour": {
        'task': 'street_food_app.tasks.log_tickets_total',
        'schedule': timedelta(seconds=10),
    },
    "every_day": {
        'task': 'street_food_app.tasks.send_mail_on_latest_tickets',
        'args': (3,),
        'schedule': timedelta(seconds=15),
    }
}

app.autodiscover_tasks()
