import asyncio

import httpx
import streamlit as st

import session_state
from menu import Menu
from main_page import MainPage


async def main():
    state = session_state.get()

    async with httpx.AsyncClient(auth=state.auth) as client:

        st.set_page_config(page_title="Wholesale Management System", layout="wide")

        MainPage.welcome()

        if state.token is None:
            MainPage.intro()

            if state.form == "register" or state.form is None:
                st.sidebar.write("Already have an account?")
                if st.sidebar.button("Sign in"):
                    state.form = "login"
            if state.form == "login":
                st.sidebar.write("Don't have an account yet?")
                if st.sidebar.button("Register"):
                    state.form = "register"

            await MainPage.form(state=state, client=client)

        else:
            st.sidebar.header("LOGOUT SECTION")
            st.sidebar.write(f"*Current session ID: {state.get_id()}*")
            if st.sidebar.button("Sign out"):
                state.clear()

            menu = await Menu.create(state=state, client=client)
            await menu.display_option()

            MainPage.info()

        state.sync()


if __name__ == "__main__":
    asyncio.run(main())
