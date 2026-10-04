from pydantic import BaseModel


class PaginatedResponse[ItemT](BaseModel):
    """One page of results plus the totals the UI needs to render pagination controls."""

    items: list[ItemT]
    total: int
    page: int
    page_size: int
