from typing import List, Optional
from datetime import date

from httpx import AsyncClient

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


async def create(client: AsyncClient, customer: CustomerCreate):
    json = {
        "customer_name": vars(customer),
    }
    return await client.post(f"{SERVER_URI}/customers/", json=json)


async def get_by_id(client: AsyncClient, customer_id: int):
    return await client.get(f"{SERVER_URI}/customers/{customer_id}")


async def get_by_name(client: AsyncClient, customer_name: str):
    params = {
        "customer_name": customer_name,
    }
    return await client.get(f"{SERVER_URI}/customers/", params=params)


async def get_all(
    client: AsyncClient, skip: Optional[int] = None, limit: Optional[int] = None
):
    params = {}
    if skip is not None:
        params["skip"] = skip
    if limit is not None:
        params["limit"] = limit
    return await client.get(f"{SERVER_URI}/customers/", params=params)


async def create_customer_transaction(
    client: AsyncClient, customer_id: int, transaction: TransactionCreate,
    transaction_details: List[TransactDetailCreate], item_name: str, shop_name: str
):
    json = {
        "transaction": vars(transaction),
        "transaction_details": [vars(detail) for detail in transaction_details],
        "item_name": item_name,
        "shop_name": shop_name,
    }
    return await client.post(f"{SERVER_URI}/{customer_id}/transactions/", json=json)


async def get_customer_transactions(client: AsyncClient, customer_id: int):
    return await client.get(f"{SERVER_URI}/{customer_id}/transactions/")
