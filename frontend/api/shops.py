from typing import List, Optional
from datetime import date

from aiohttp import ClientSession

from api import BASE_URL, Response


class ShopCreate:

    def __init__(self, name: str):
        self.shop_name = name


class ImportationCreate:

    def __init__(self, date: date):
        self.date = date


class ImportDetailCreate:

    def __init__(self, item_amount: int):
        self.item_amount = item_amount


async def create(session: ClientSession, shop: ShopCreate):
    json = {
        "shop_name": vars(shop),
    }
    async with session.post(f"{BASE_URL}/shops/", json=json) as response:
        status = response.status,
        data = await response.json()
        return Response(status, data)


async def get_by_id(session: ClientSession, shop_id: int):
    async with session.get(f"{BASE_URL}/shops/{shop_id}") as response:
        status = response.status,
        data = await response.json()
        return Response(status, data)


async def get_by_name(session: ClientSession, shop_name: str):
    params = {
        "shop_name": shop_name,
    }
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
        status = response.status
        data = await response.json()
        return Response(status, data)


async def create_shop_importation(session: ClientSession, shop_id: int,
                                  importation: ImportationCreate,
                                  importation_details: List[ImportDetailCreate],
                                  item_name: str):
    json = {
        "importation": vars(importation),
        "importation_details": [vars(detail) for detail in importation_details],
        "item_name": item_name,
    }
    async with session.post(f"{BASE_URL}/{shop_id}/importations/", json=json) as response:
        status = response.status
        data = await response.json()
        return Response(status, data)


async def get_shop_importations(session: ClientSession, shop_id: int):
    async with session.get(f"{BASE_URL}/{shop_id}/importations/") as response:
        status = response.status
        data = await response.json()
        return Response(status, data)


async def get_shop_transactions(session: ClientSession, shop_id: int):
    async with session.get(f"{BASE_URL}/{shop_id}/transactions/") as response:
        status = response.status
        data = await response.json()
        return Response(status, data)


async def get_shop_items(session: ClientSession, shop_id: int):
    async with session.get(f"{BASE_URL}/{shop_id}/items/") as response:
        status = response.status
        data = await response.json()
        return Response(status, data)
