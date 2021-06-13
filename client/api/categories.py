from typing import Optional

from aiohttp import ClientSession

from api import BASE_URL, Response


async def get_by_uid(session: ClientSession, category_uid: int):
    async with session.get(f"{BASE_URL}/categories/{category_uid}") as response:
        status = response.status,
        data = await response.json()
        return Response(status, data)


async def get_by_name(session: ClientSession, category_name: str):
    params = {"category_name": category_name}
    async with session.get(f"{BASE_URL}/categories/", params=params) as response:
        status = response.status,
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
    async with session.get(f"{BASE_URL}/categories/", params=params) as response:
        status = response.status,
        data = await response.json()
        return Response(status, data)


async def get_items_of_category(session: ClientSession, category_uid: int):
    async with session.get(f"{BASE_URL}/{category_uid}/items/") as response:
        status = response.status,
        data = await response.json()
        return Response(status, data)
