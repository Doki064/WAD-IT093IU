from typing import List, Optional
from datetime import date

from httpx import AsyncClient

from core.config import SERVER_URI


class ShopCreate:
    def __init__(self, name: str):
        self.shop_name = name


class ImportationCreate:
    def __init__(self, date: date):
        self.date = date


class ImportDetailCreate:
    def __init__(self, item_amount: int):
        self.item_amount = item_amount


async def create(client: AsyncClient, shop: ShopCreate):
    json = {
        "shop_name": vars(shop),
    }
    return await client.post(f"{SERVER_URI}/shops/", json=json)


async def get_by_id(client: AsyncClient, shop_id: int):
    return await client.get(f"{SERVER_URI}/shops/{shop_id}")


async def get_by_name(client: AsyncClient, shop_name: str):
    params = {
        "shop_name": shop_name,
    }
    return await client.get(f"{SERVER_URI}/shops/", params=params)


async def get_all(
    client: AsyncClient, skip: Optional[int] = None, limit: Optional[int] = None
):
    params = {}
    if skip is not None:
        params["skip"] = skip
    if limit is not None:
        params["limit"] = limit
    return await client.get(f"{SERVER_URI}/shops/", params=params)


async def create_shop_importation(
    client: AsyncClient, shop_id: int, importation: ImportationCreate,
    importation_details: List[ImportDetailCreate], item_name: str
):
    json = {
        "importation": vars(importation),
        "importation_details": [vars(detail) for detail in importation_details],
        "item_name": item_name,
    }
    return await client.post(f"{SERVER_URI}/{shop_id}/importations/", json=json)


async def get_shop_importations(client: AsyncClient, shop_id: int):
    return await client.get(f"{SERVER_URI}/{shop_id}/importations/")


async def get_shop_transactions(client: AsyncClient, shop_id: int):
    return await client.get(f"{SERVER_URI}/{shop_id}/transactions/")


async def get_shop_items(client: AsyncClient, shop_id: int):
    return await client.get(f"{SERVER_URI}/{shop_id}/items/")
