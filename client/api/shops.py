from typing import Optional

from aiohttp import ClientSession

from api import BASE_URL, Response


async def get_by_uid(session: ClientSession, shop_uid: int):
    async with session.get(f"{BASE_URL}/shops/{shop_uid}") as response:
        status = response.status,
        data = await response.json()
        return Response(status, data)


async def get_by_name(session: ClientSession, shop_name: str):
    params = {"shop_name": shop_name}
    async with session.get(f"{BASE_URL}/shops/", params=params) as response:
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
    async with session.get(f"{BASE_URL}/shops/", params=params) as response:
        status = response.status,
        data = await response.json()
        return Response(status, data)


async def get_importations_of_shop(session: ClientSession, shop_uid: int):
    async with session.get(f"{BASE_URL}/{shop_uid}/importations/") as response:
        status = response.status,
        data = await response.json()
        return Response(status, data)


async def get_transactions_of_shop(session: ClientSession, shop_uid: int):
    async with session.get(f"{BASE_URL}/{shop_uid}/transactions/") as response:
        status = response.status,
        data = await response.json()
        return Response(status, data)


async def get_items_of_shop(session: ClientSession, shop_uid: int):
    async with session.get(f"{BASE_URL}/{shop_uid}/items/") as response:
        status = response.status,
        data = await response.json()
        return Response(status, data)
