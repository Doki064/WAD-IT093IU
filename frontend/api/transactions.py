from typing import Optional
from datetime import date

from httpx import AsyncClient


async def get_by_id(client: AsyncClient, transaction_id: int):
    return await client.get(f"/transactions/{transaction_id}")


async def get_by_date(client: AsyncClient, date: date):
    return await client.get(f"/transactions/date/{date}")


async def get_all(
    client: AsyncClient, skip: Optional[int] = None, limit: Optional[int] = None
):
    params = {}
    if skip is not None:
        params["skip"] = skip
    if limit is not None:
        params["limit"] = limit
    return await client.get("/transactions", params=params)


async def get_details(client: AsyncClient, transaction_id: int):
    return await client.get(f"/transactions/{transaction_id}/details")


async def get_min_max_dates(client: AsyncClient):
    return await client.get("/transactions/min-max-dates")
