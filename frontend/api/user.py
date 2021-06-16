from aiohttp import ClientSession

from api import Response
from core.config import SERVER_URI


async def login(session: ClientSession, username: str, password: str):
    json = {
        "username": username,
        "password": password,
    }
    async with session.post(f"{SERVER_URI}/users/login/", json=json) as response:
        status = response.status
        data = await response.json()
        return Response(status, data)


async def register(session: ClientSession, username: str, password: str):
    json = {
        "username": username,
        "password": password,
    }
    async with session.post(f"{SERVER_URI}/users/register/", json=json) as response:
        status = response.status
        data = await response.json()
        return Response(status, data)
