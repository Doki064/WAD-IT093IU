from typing import Optional

import orjson
from httpx import AsyncClient


class CategoryCreate:
    def __init__(self, name: str):
        self.category_name = name


class ItemCreate:
    def __init__(self, name: str, quantity: int):
        self.item_name = name
        self.quantity = quantity


async def create(client: AsyncClient, category: CategoryCreate):
    data = {
        "category_name": vars(category),
    }
    return await client.post("/categories", content=orjson.dumps(data))


async def get_by_id(client: AsyncClient, category_id: int):
    return await client.get(f"/categories/{category_id}")


async def get_by_name(client: AsyncClient, category_name: str):
    params = {
        "category_name": category_name,
    }
    return await client.get("/categories", params=params)


async def get_all(
    client: AsyncClient, skip: Optional[int] = None, limit: Optional[int] = None
):
    params = {}
    if skip is not None:
        params["skip"] = skip
    if limit is not None:
        params["limit"] = limit
    return await client.get("/categories", params=params)


async def create_category_item(
    client: AsyncClient, category_id: int, item: ItemCreate, shop_name: str
):
    data = {
        "item": vars(item),
        "shop_name": shop_name,
    }
    return await client.post(f"/{category_id}/items", content=orjson.dumps(data))


async def get_category_items(client: AsyncClient, category_id: int):
    return await client.get(f"/{category_id}/items")
