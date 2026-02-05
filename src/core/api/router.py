from fastapi import APIRouter, Depends, status

from core.api import crud
from core.api.schemes import params, schemes


class Router:

    def __init__(self):
        self.router = APIRouter()
        self.setup_routes()

    def setup_routes(self):
        pass

class CurrencyDataAPI(Router):


    def setup_routes(self):

        @self.router.get(
            "/prices",
            response_model=schemes.CurrencyHistoricalData,
            status_code=status.HTTP_200_OK
        )
        async def get_historical_prices(ticker: str, pagination: params.Pagination = Depends()):
            return await crud.get_histiorical_prices(ticker, pagination)


        @self.router.get(
            "/price",
            response_model=schemes.CurrencyResponse,
            status_code=status.HTTP_200_OK
        )
        async def get_price(params: params.GetPrice = Depends()):
            return await crud.get_currency(**params.model_dump(by_alias=True))
        
service = CurrencyDataAPI()