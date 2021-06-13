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
        state = session_state.get(token={}, plot={})

        st.set_page_config(page_title="Wholesale Management System", layout="wide")

        mainpage = MainPage()
        mainpage.call()

        if state.token is None:
            mainpage.intro()

            st.sidebar.header("LOGIN SECTION")
            st.sidebar.subheader("**WARNING: AUTHORIZED ACCESS ONLY**")
            st.sidebar.write("Please **login** first to use the application")

            with st.form("login_form"):
                state.username = st.sidebar.text_input("Username: ",
                                                       value=state.username or "",
                                                       key="login_username")
                password = st.sidebar.text_input("Password: ",
                                                 type="password",
                                                 value="",
                                                 key="login_password")
                submitted = st.form_submit_button("Submit")
                if submitted and state.username and password:
                    url = f"http://{REQUEST_HOST}:{REQUEST_PORT}/api/users/login/"
                    login_user = {
                        "username": state.username,
                        "password": password,
                    }
                    async with session.post(url, json=login_user) as response:
                        if response.status == 200:
                            pass
                        elif response.status == 401:
                            st.warning("The username or password was not correct")
                            st.stop()
                        else:
                            st.error(response.status)
                            err = await response.json()
                            st.error(err["detail"])

            # if st.sidebar.button("Sign in"):
            #     if not encryption.check_password(security_key, state.login_key):
            #         with st.sidebar.warning("Wrong password!"):
            #             sleep(1)
            #             state.clear()
            #     else:
            #         state.remove('login_key')
            #         state.is_login = True
            #         st.experimental_rerun()

        else:
            st.sidebar.header("LOGOUT SECTION")
            st.sidebar.write(f"*Current session ID: {state.get_id()}*")
            if st.sidebar.button("Sign out"):
                state.clear()

            menu = Menu(state=state, session=session)
            menu.display_option()

            mainpage.info()

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
