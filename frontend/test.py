import asyncio

import httpx
from httpx_auth import OAuth2ResourceOwnerPasswordCredentials


# flake8: noqa
async def get_token():
    auth = OAuth2ResourceOwnerPasswordCredentials(
        "http://localhost:8080/api/v1/users/login/auth", "admin", "admin"
    )
    async with httpx.AsyncClient() as client:
        # headers = {"content-type": "application/x-www-form-urlencoded"}
        data = {"username": "admin", "password": "admin"}
        response = await client.post(
            "http://localhost:8080/api/v1/users/login/auth", data=data
        )
        print(response)
        print(response.json())


asyncio.run(get_token())
