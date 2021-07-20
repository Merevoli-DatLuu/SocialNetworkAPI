from __future__ import absolute_import, unicode_literals
import os
from celery import Celery, shared_task
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_network.settings')

app = Celery('social_network', broker="redis://localhost:6379/0")
app.config_from_object('django.conf:settings', namespace='CELERY_SOCIAL_NETWORK')
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
  print('Request: {0!r}'.format(self.request))

app.conf.beat_schedule = {
    'delete-expired-post-every-morning': {
        'task': 'delete-post',
        'schedule': crontab(hour=8, minute=0),
    }
}