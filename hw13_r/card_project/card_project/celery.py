from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'card_project.settings')

app = Celery('card__project')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    # Define the periodic task to freeze expired cards every day at midnight
    'freeze_expired_cards': {
        'task': 'cards.tasks.freeze_expired_cards',
        'schedule': crontab(minute=0, hour=0),
    },
}