import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "street_food_project.settings")

app = Celery("street_food_project")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
