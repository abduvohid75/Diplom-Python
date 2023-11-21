from __future__ import absolute_import, unicode_literals
from celery import Celery
from datetime import timedelta
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'secrets': {
        'task': 'secret.tasks.kill_secret',
        'schedule': timedelta(minutes=1),
    },
}

app.autodiscover_tasks()
