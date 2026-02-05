import aiohttp
from datetime import timedelta
import json

from common_types import datetime, UTC
from core.loader.schemes import schemes
from db import dao


from logger import setup_logger

logs = setup_logger(__name__)


async def get_data(url, params):
    async with aiohttp.ClientSession() as session:
        while True:

            try:
                async with session.get(url, params=params) as response:

                    try:
                        data = await response.json()
                    except json.JSONDecodeError as e:
                        logs.warning(f"Fail to load price. Detail: {e.msg}, args: {e.args}")
                        continue
                    if data.get("error", {}).get("code") == 10028:
                        continue
                    else: 
                        return data
            except aiohttp.ClientError as e:
                logs.warning(f"Fail to load price. Detail: {e.__traceback__}, args: {e.args}")
                break


def price_monitoring(last_price_timestamp: datetime):
    return datetime.now(tz=UTC) - last_price_timestamp <= timedelta(minutes=1)

async def load(index_name):
    
    accuracy_step = 2
    period = "2h"
    while True:
        last_price = await dao.get_price(index_name)

        if price_monitoring(last_price.timestamp):
            logs.info("price monitoring")
            break

        if datetime.now(tz=UTC) - last_price.timestamp <= timedelta(hours=1):
            accuracy_step = 10
            period = "1h"
        elif datetime.now(tz=UTC) - last_price.timestamp <= timedelta(days=1):
            accuracy_step = 1
            period = "1d"
        else:
            accuracy_step = 1
            period = "2d"

        arch_data = await get_data(
            "https://test.deribit.com/api/v2/public/get_index_chart_data",
            params={
                "index_name": index_name,
                "range": period
            }
        )
        results = arch_data.get("result")
        total = len(results)
        for i in range(0, total, accuracy_step):
            timestamp, price = results[i]
            timestamp = datetime.fromtimestamp(timestamp/1000, tz=UTC)
            if timestamp <= last_price.timestamp:
                continue

            await dao.save_current_price(
                schemes.Currency(
                    price=price, 
                    currency=index_name,
                    timestamp=timestamp,
                )
            )
            if price_monitoring(timestamp):
                break