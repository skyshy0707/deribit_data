from celery import Celery

from core.loader import settings

app = Celery('load_price')
app.config_from_object(settings, namespace='CELERY')
app.autodiscover_tasks()