from typing import List

from pydantic import BaseModel

from common_types import datetime
from core.api.schemes.params import Pagination

from logger import setup_logger

logger = setup_logger(__name__)

class CurrencyResponseItem(BaseModel):
    price: float
    timestamp: datetime

class CurrencyResponse(CurrencyResponseItem):
    currency: str

class CurrencyItemsData(Pagination):
    items: List[CurrencyResponseItem]
    total: int

class CurrencyHistoricalData(BaseModel):
    ticker: str
    data: CurrencyItemsData