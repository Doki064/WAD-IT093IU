from typing import Optional

from aiohttp import ClientSession

from api import BASE_URL, Response


async def get_by_uid(session: ClientSession, customer_uid: int):
    async with session.get(f"{BASE_URL}/customers/{customer_uid}") as response:
        status = response.status,
        data = await response.json()
        return Response(status, data)


async def get_by_name(session: ClientSession, customer_name: str):
    params = {"customer_name": customer_name}
    async with session.get(f"{BASE_URL}/customers/", params=params) as response:
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
    async with session.get(f"{BASE_URL}/customers/", params=params) as response:
        status = response.status,
        data = await response.json()
        return Response(status, data)


async def get_transactions_of_customer(session: ClientSession, customer_uid: int):
    async with session.get(f"{BASE_URL}/{customer_uid}/transactions/") as response:
        status = response.status,
        data = await response.json()
        return Response(status, data)
