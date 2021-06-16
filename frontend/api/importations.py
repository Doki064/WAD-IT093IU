from typing import Optional
from datetime import date

from httpx import AsyncClient

from core.config import SERVER_URI


async def get_by_id(client: AsyncClient, importation_id: int):
    return await client.get(f"{SERVER_URI}/importations/{importation_id}")


async def get_by_date(client: AsyncClient, date: date):
    return await client.get(f"{SERVER_URI}/importations/date/{date}")


async def get_all(
    client: AsyncClient, skip: Optional[int] = None, limit: Optional[int] = None
):
    params = {}
    if skip is not None:
        params["skip"] = skip
    if limit is not None:
        params["limit"] = limit
    return await client.get(f"{SERVER_URI}/importations/", params=params)


async def get_details(client: AsyncClient, importation_id: int):
    return await client.get(f"{SERVER_URI}/{importation_id}/details/")
