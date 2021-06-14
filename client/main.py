import asyncio
import os
from pathlib import Path

import orjson
import aiohttp
import streamlit as st
from dotenv import load_dotenv

import session_state
from menu import Menu
from main_page import MainPage
# from management import Management
# from plot import Plot
# from table import Table

BASE_DIR = Path(__file__).absolute().parent
load_dotenv(BASE_DIR.joinpath(".env"))

REQUEST_HOST = os.environ["REQUEST_HOST"]
REQUEST_PORT = os.environ["REQUEST_PORT"]


async def main():
    async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
        state = session_state.get(token={}, form="register")

        st.set_page_config(page_title="Wholesale Management System", layout="wide")

        MainPage.welcome()

        if not state.token:
            MainPage.intro()

            if state.form == "register":
                st.sidebar.write("Already have an account?")
                if st.sidebar.button("Sign in"):
                    state.form = "login"
            if state.form == "login":
                st.sidebar.write("Don't have an account yet?")
                if st.sidebar.button("Register"):
                    state.form = "register"

            await MainPage.form(state, session)

        else:
            st.sidebar.header("LOGOUT SECTION")
            st.sidebar.write(f"*Current session ID: {state.get_id()}*")
            if st.sidebar.button("Sign out"):
                state.clear()

            menu = Menu(state=state, session=session)
            menu.display_option()

            MainPage.info()

        state.sync()


def get_or_create_event_loop():
    try:
        return asyncio.get_event_loop()
    except RuntimeError as e:
        if "There is no current event loop in thread" in str(e):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return asyncio.get_event_loop()


if __name__ == "__main__":
    loop = get_or_create_event_loop()
    loop.run_until_complete(main())
