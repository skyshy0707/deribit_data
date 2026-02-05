import asyncio

from config import OBSERVED_TICKERS
from core.loader.celery import app
from core.loader import loader

@app.task
def loading_currency_price():
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    tasks = [] 

    for index in OBSERVED_TICKERS:
        tasks.append(
            loop.create_task(loader.load(index))
        )

    result = loop.run_until_complete(asyncio.wait(tasks))

    return 'Done'