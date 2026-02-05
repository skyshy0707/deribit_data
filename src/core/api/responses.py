from fastapi import status
from fastapi.exceptions import HTTPException


def raise_(http_exc: HTTPException):
    raise http_exc

NOT_FOUND = lambda detail: raise_(
    HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Not found. Detail: {detail}"
    )
)