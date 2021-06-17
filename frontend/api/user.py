from httpx import AsyncClient

from core.config import SERVER_URI


async def login(client: AsyncClient, username: str, password: str):
    data = {
        "username": username,
        "password": password,
    }
    return await client.post(f"{SERVER_URI}/users/login/auth", data=data)


async def register(client: AsyncClient, username: str, password: str):
    json = {
        "username": username,
        "password": password,
    }
    return await client.post(f"{SERVER_URI}/users/register", json=json)
