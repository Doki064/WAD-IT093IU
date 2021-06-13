import asyncio

import aiohttp
import pandas as pd
import streamlit as st


async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get("http://localhost:8080/api/") as response:
            data = await response.json()
            st.header(data["message"])

        username = st.text_input("Username: ", value="")
        password = st.text_input("Password: ", value="")
        user = {"username": username, "password": password}

        resp = st.empty()
        if st.button("Register") and username and password:
            async with session.post("http://localhost:8080/api/users/register/",
                                    json=user) as response:
                if response.status == 200:
                    resp.write(response.status)
                    resp.write(await response.json())
                else:
                    resp.exception(response.status)
                    resp.exception(await response.json())

        if st.button("Get table"):
            async with session.get(
                    "http://localhost:8080/api/internal/admin/") as response:
                if response.status == 200:
                    st.write(response.status)
                    df = pd.json_normalize(await response.json())
                    st.write(df.transpose())
                else:
                    st.exception(response.status)
                    st.exception(await response.json())


def get_or_create_eventloop():
    try:
        return asyncio.get_event_loop()
    except RuntimeError as e:
        if "There is no current event loop in thread" in str(e):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return asyncio.get_event_loop()


if __name__ == "__main__":
    loop = get_or_create_eventloop()
    loop.run_until_complete(main())
