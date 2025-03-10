from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

"""
Celery configuration module
"""

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BarberShop.settings')
app = Celery('BarberShop')
app.conf.enable_utc = False
app.conf.update(timezone = 'Asia/Tehran')
app.config_from_object(settings, namespace='CELERY')


#Celery Beat Settings
app.conf.beat_schedule = {}

app.autodiscover_tasks(['users', ])

@app.task(bind=True)
def debug_task(self):
    print(f'{self.request!r}')


