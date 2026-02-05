from core.loader.tasks import app

app.conf.beat_schedule = {
    'monitor_currency_price': {
        'task': 'core.loader.tasks.loading_currency_price',
        'schedule': 60
    }
}