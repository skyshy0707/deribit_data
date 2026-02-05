import os

from kombu import Exchange, Queue


REDIS_HOST = 'broker'
REDIS_PORT = '6379'

CELERY_BROKER_URL = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'
CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
CELERY_RESULT_BACKEND = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'

CELERY_DEFAULT_QUEUE = 'default'
CELERY_ENABLE_UTC = False
CELERY_TIMEZONE = os.environ.get("TZ")

CELERY_QUEUES = (
    Queue("default", Exchange("default"), routing_key="default"),
    Queue("monitor_currency_price", Exchange("monitor_currency_price"), routing_key="monitor_currency_price")
)

CELERY_ROUTES = {
    "loader.tasks.loading_currency_price": {
        "queue": "monitor_currency_price"
    }
}