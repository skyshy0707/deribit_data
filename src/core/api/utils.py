from core.api.schemes.params import Pagination

def paginate_qs(qs: list, pagination_params: Pagination) -> dict:

    limit = pagination_params.limit
    offset = pagination_params.offset
    items = list(qs)
    return {
        "limit": limit,
        "offset": offset + limit,
        "total": len(items),
        "items": items[offset : limit+offset]
    }