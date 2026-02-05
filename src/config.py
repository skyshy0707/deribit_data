import os

from pydantic import BaseModel

OBSERVED_TICKERS = [
    "btc_usd",
    "eth_usd"
]

class database(BaseModel):

    POSTGRES_DB_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_DB_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB_HOST: str = os.getenv("POSTGRES_HOST")
    POSTGRES_DB_NAME: str = os.getenv("POSTGRES_DB")
    
db = database()