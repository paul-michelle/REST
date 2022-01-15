from __future__ import absolute_import, unicode_literals
from street_food_project.celery_service import app as celery_app

__all__ = (
    "celery_app",
)