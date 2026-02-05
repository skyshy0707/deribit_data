import httpx
import pytest
import pytest_asyncio
from typing import AsyncIterator


@pytest_asyncio.fixture
async def client() -> AsyncIterator[httpx.AsyncClient]:
    async with httpx.AsyncClient(base_url="http://127.0.0.1:8000/api") as client:
        yield client

@pytest.mark.asyncio
async def test_prices(client: httpx.AsyncClient):
    ticker = "btc_usd"
    response = await client.get("/prices", params={
        "ticker": ticker
    })
    data = response.json()
    assert response.status_code == 200
    assert data.get("ticker") == ticker


@pytest.mark.asyncio
async def test_price(client: httpx.AsyncClient):
    ticker = "btc_usd"
    response = await client.get("/price", params={
        "ticker": ticker
    })
    data = response.json()
    assert (response.status_code == 200 or response.status_code == 404)
    
    if response.status_code == 200:
        assert data.get("currency") == ticker