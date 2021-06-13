from typing import Optional

from aiohttp import ClientSession

from api import BASE_URL, Response


async def get_by_uid(session: ClientSession, item_uid: int):
    async with session.get(f"{BASE_URL}/items/{item_uid}") as response:
        status = response.status
        data = await response.json()
        return Response(status, data)


async def get_by_name(session: ClientSession, item_name: str):
    params = {
        "item_name": item_name,
    }
    async with session.get(f"{BASE_URL}/items/", params=params) as response:
        status = response.status
        data = await response.json()
        return Response(status, data)


async def get_all(session: ClientSession,
                  skip: Optional[int] = None,
                  limit: Optional[int] = None):
    params = {}
    if skip is not None:
        params["skip"] = skip
    if limit is not None:
        params["limit"] = limit
    async with session.get(f"{BASE_URL}/items/", params=params) as response:
        status = response.status
        data = await response.json()
        return Response(status, data)
