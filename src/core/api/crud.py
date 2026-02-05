from core.api.utils import paginate_qs
from core.api.schemes import params
from core.api import responses
from db import dao


async def get_currency(currency: str, date: str=None):
    data = await dao.get_price(currency, date)
    if not data:
        return responses.NOT_FOUND(f"Data are not exist for this instrument: {currency} or at this time: {date}")
    return data

async def get_histiorical_prices(currency: str, pagination: params.Pagination):
    prices = await dao.prices(currency)
    return {
        "ticker": currency,
        "data": paginate_qs(prices, pagination)
    }