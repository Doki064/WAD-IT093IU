from typing import Optional
from datetime import date

from aiohttp import ClientSession

from api import Response
from core.config import SERVER_URI


async def get_by_id(session: ClientSession, transaction_id: int):
    async with session.get(f"{SERVER_URI}/transactions/{transaction_id}") as response:
        status = response.status
        data = await response.json()
        return Response(status, data)


async def get_by_date(session: ClientSession, date: date):
    async with session.get(f"{SERVER_URI}/transactions/date/{date}") as response:
        status = response.status
        data = await response.json()
        return Response(status, data)


async def get_all(
    session: ClientSession, skip: Optional[int] = None, limit: Optional[int] = None
):
    params = {}
    if skip is not None:
        params["skip"] = skip
    if limit is not None:
        params["limit"] = limit
    async with session.get(f"{SERVER_URI}/transactions/", params=params) as response:
        status = response.status
        data = await response.json()
        return Response(status, data)


async def get_details(session: ClientSession, transaction_id: int):
    async with session.get(f"{SERVER_URI}/{transaction_id}/details/") as response:
        status = response.status
        data = await response.json()
        return Response(status, data)
