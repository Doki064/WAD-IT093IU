from typing import Optional

from aiohttp import ClientSession

from api import Response
from core.config import SERVER_URI


class CategoryCreate:
    def __init__(self, name: str):
        self.category_name = name


class ItemCreate:
    def __init__(self, name: str, quantity: int):
        self.item_name = name
        self.quantity = quantity


async def create(session: ClientSession, category: CategoryCreate):
    json = {
        "category_name": vars(category),
    }
    async with session.post(f"{SERVER_URI}/categories/", json=json) as response:
        status = response.status
        data = await response.json()
        return Response(status, data)


async def get_by_id(session: ClientSession, category_id: int):
    async with session.get(f"{SERVER_URI}/categories/{category_id}") as response:
        status = response.status,
        data = await response.json()
        return Response(status, data)


async def get_by_name(session: ClientSession, category_name: str):
    params = {
        "category_name": category_name,
    }
    async with session.get(f"{SERVER_URI}/categories/", params=params) as response:
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
    async with session.get(f"{SERVER_URI}/categories/", params=params) as response:
        status = response.status
        data = await response.json()
        return Response(status, data)


async def create_category_item(
    session: ClientSession, category_id: int, item: ItemCreate, shop_name: str
):
    json = {
        "item": vars(item),
        "shop_name": shop_name,
    }
    async with session.post(f"{SERVER_URI}/{category_id}/items/", json=json) as response:
        status = response.status
        data = await response.json()
        return Response(status, data)


async def get_category_items(session: ClientSession, category_id: int):
    async with session.get(f"{SERVER_URI}/{category_id}/items/") as response:
        status = response.status
        data = await response.json()
        return Response(status, data)
