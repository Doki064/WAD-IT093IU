from typing import Optional

from httpx import AsyncClient


async def get_by_id(client: AsyncClient, item_id: int):
    return await client.get(f"/items/{item_id}")


async def get_by_name(client: AsyncClient, item_name: str):
    params = {
        "item_name": item_name,
    }
    return await client.get("/items", params=params)


async def get_all(
    client: AsyncClient, skip: Optional[int] = None, limit: Optional[int] = None
):
    params = {}
    if skip is not None:
        params["skip"] = skip
    if limit is not None:
        params["limit"] = limit
    return await client.get("/items", params=params)
