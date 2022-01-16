import os
import celery
from datetime import timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "street_food_project.settings")

app = celery.Celery("street_food_project")
app.config_from_object("django.conf:settings", namespace='CELERY')

app.conf.beat_schedule = {
    "every_day": {
        'task': 'street_food_app.tasks.send_mail_with_tickets_count',
        'schedule': timedelta(seconds=float(os.environ.get('EMAIL_INTERVAL_SECONDS', '86400'))),
    }
}

app.autodiscover_tasks()
