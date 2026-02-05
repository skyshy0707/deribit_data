from typing import Optional

from fastapi import Query
from pydantic import BaseModel, field_serializer

from common_types import datetime

def to_date(datestr) -> str:
    date = datetime.now()
    
    try:
        date = datetime.fromisoformat(datestr)

    except ValueError:
        try:
            date = datetime.strptime(datestr, "%d.%m.%Y")
        except ValueError:
            try:
                date = datetime.strptime(datestr, "%d.%m.%Y.%H:%M")
            except Exception:
                pass

    return date.isoformat()
    

class Pagination(BaseModel):
    limit: int = Query(10, gt=0, le=10)
    offset: int = Query(0, ge=0)

class GetPrice(BaseModel):
    ticker: str = Query(serialization_alias="currency")
    timestamp: Optional[str] = Query('', serialization_alias="date")

    @field_serializer('timestamp')
    def serialize_timestamp(self, value: str):
        return to_date(value)