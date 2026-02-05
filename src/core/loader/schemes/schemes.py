from common_types import datetime, UTC

from pydantic import AliasChoices, AliasPath, BaseModel, Field

class Currency(BaseModel):
    price: float = Field(validation_alias=AliasChoices("price", AliasPath("result", "index_price")))
    currency: str
    timestamp: datetime = Field(default=datetime.now(tz=UTC))