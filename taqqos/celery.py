from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taqqos.settings')

app = Celery('taqqos')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Load tasks from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    "sync_business_subscriptions": {
        "task": "taqqos.product.tasks.match_product_price",
        "schedule": crontab(minute='*/30'),
    },
}