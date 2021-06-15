import asyncio

import orjson
import aiohttp
import streamlit as st

import session_state
from menu import Menu
from main_page import MainPage


async def main():
    async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
        state = session_state.get()

        st.set_page_config(page_title="Wholesale Management System", layout="wide")

        MainPage.welcome()

        if state.token is None:
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


if __name__ == "__main__":
    asyncio.run(main())
