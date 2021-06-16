from typing import List, Optional
from datetime import date

from aiohttp import ClientSession

from api import Response
from core.config import SERVER_URI


class CustomerCreate:
    def __init__(self, name: str):
        self.customer_name = name


class TransactionCreate:
    def __init__(self, date: date, status: str):
        self.date = date
        self.status = status


class TransactDetailCreate:
    def __init__(self, item_price: float, item_amount: int):
        self.item_price = item_price
        self.item_amount = item_amount


async def create(session: ClientSession, customer: CustomerCreate):
    json = {
        "customer_name": vars(customer),
    }
    async with session.post(f"{SERVER_URI}/customers/", json=json) as response:
        status = response.status,
        data = await response.json()
        return Response(status, data)


async def get_by_id(session: ClientSession, customer_id: int):
    async with session.get(f"{SERVER_URI}/customers/{customer_id}") as response:
        status = response.status
        data = await response.json()
        return Response(status, data)


async def get_by_name(session: ClientSession, customer_name: str):
    params = {
        "customer_name": customer_name,
    }
    async with session.get(f"{SERVER_URI}/customers/", params=params) as response:
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
    async with session.get(f"{SERVER_URI}/customers/", params=params) as response:
        status = response.status
        data = await response.json()
        return Response(status, data)


async def create_customer_transaction(
    session: ClientSession, customer_id: int, transaction: TransactionCreate,
    transaction_details: List[TransactDetailCreate], item_name: str, shop_name: str
):
    json = {
        "transaction": vars(transaction),
        "transaction_details": [vars(detail) for detail in transaction_details],
        "item_name": item_name,
        "shop_name": shop_name,
    }
    async with session.post(
        f"{SERVER_URI}/{customer_id}/transactions/", json=json
    ) as response:
        status = response.status
        data = await response.json()
        return Response(status, data)


async def get_customer_transactions(session: ClientSession, customer_id: int):
    async with session.get(f"{SERVER_URI}/{customer_id}/transactions/") as response:
        status = response.status
        data = await response.json()
        return Response(status, data)
