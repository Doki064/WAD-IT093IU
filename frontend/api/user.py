from httpx import AsyncClient

import orjson


async def login(client: AsyncClient, username: str, password: str):
    data = {
        "username": username,
        "password": password,
    }
    return await client.post("/users/login/auth", data=orjson.dumps(data))


async def register(client: AsyncClient, username: str, password: str):
    data = {
        "username": username,
        "password": password,
    }
    return await client.post("/users/register", data=orjson.dumps(data))
