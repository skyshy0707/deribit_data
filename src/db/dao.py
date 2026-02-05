from sqlalchemy import insert, select, desc, Select
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, DBAPIError
from sqlalchemy.ext.asyncio import AsyncSession

from common_types import datetime
from config import OBSERVED_TICKERS
from core.loader.schemes import schemes
from db import models
from db.engine import connection


from logger import setup_logger
logger = setup_logger(__name__)

@connection(commit=True)
async def create_currencies(session: AsyncSession):
    for index in OBSERVED_TICKERS:
        try:
            await session.execute(insert(models.Currency).values(ticker=index))
        except IntegrityError as e:
            if "unique" in e._message().lower():
                continue
        except DBAPIError:
            continue
    logger.info("Currencies were created")


def get_prices_q(currency: str) -> Select:
    return select(models.Price).where(
        models.Price.currency==currency
    ).order_by(desc(models.Price.timestamp))

@connection(commit=True)
async def save_current_price(session: AsyncSession, price_data: schemes.Currency):
    data = price_data.model_dump()
    try:
        await session.execute(insert(models.Price).values(**data).returning(models.Price))
    except SQLAlchemyError as e:
        logger.warning(f"error occur at {e._message()}")
        raise SQLAlchemyError(e)
    else:
        logger.info(f"Data {data} were loaded")
    
@connection()
async def get_price(session: AsyncSession, currency: str, date: datetime=None):
    if not date:
        date = datetime.now().isoformat()
    return (
        await session.execute(
            get_prices_q(currency).where(models.Price.timestamp <= datetime.fromisoformat(date)).limit(1)
        )
    ).scalar_one_or_none()

@connection()
async def prices(session: AsyncSession, currency: str):

    return (
        await session.execute(get_prices_q(currency))
    ).scalars()