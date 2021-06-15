from aiohttp import ClientSession

from api import BASE_URL, Response


async def login(session: ClientSession, username: str, password: str):
    json = {
        "username": username,
        "password": password,
    }
    async with session.post(f"{BASE_URL}/users/login/", json=json) as response:
        status = response.status
        data = await response.json()
        return Response(status, data)


async def register(session: ClientSession, username: str, password: str):
    json = {
        "username": username,
        "password": password,
    }
    async with session.post(f"{BASE_URL}/users/register/", json=json) as response:
        status = response.status
        data = await response.json()
        return Response(status, data)
