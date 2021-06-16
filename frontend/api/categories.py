from typing import Optional

from httpx import AsyncClient

from core.config import SERVER_URI


class CategoryCreate:
    def __init__(self, name: str):
        self.category_name = name


class ItemCreate:
    def __init__(self, name: str, quantity: int):
        self.item_name = name
        self.quantity = quantity


async def create(client: AsyncClient, category: CategoryCreate):
    json = {
        "category_name": vars(category),
    }
    return await client.post(f"{SERVER_URI}/categories/", json=json)


async def get_by_id(client: AsyncClient, category_id: int):
    return await client.get(f"{SERVER_URI}/categories/{category_id}")


async def get_by_name(client: AsyncClient, category_name: str):
    params = {
        "category_name": category_name,
    }
    return await client.get(f"{SERVER_URI}/categories/", params=params)


async def get_all(
    client: AsyncClient, skip: Optional[int] = None, limit: Optional[int] = None
):
    params = {}
    if skip is not None:
        params["skip"] = skip
    if limit is not None:
        params["limit"] = limit
    return await client.get(f"{SERVER_URI}/categories/", params=params)


async def create_category_item(
    client: AsyncClient, category_id: int, item: ItemCreate, shop_name: str
):
    json = {
        "item": vars(item),
        "shop_name": shop_name,
    }
    return await client.post(f"{SERVER_URI}/{category_id}/items/", json=json)


async def get_category_items(client: AsyncClient, category_id: int):
    return await client.get(f"{SERVER_URI}/{category_id}/items/")
