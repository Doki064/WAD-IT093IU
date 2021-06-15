"""
Example:
    >>> import main_page
    >>> main_page = gui.MainPage()
    >>> gui.intro() # Display the intro section
    >>> gui.info() # Display the info on the sidebar
"""

import re

import streamlit as st
from aiohttp import ClientSession

from session_state import SessionState
from api import user


class MainPage:
    """Main Page of the Web App

    The main page displays the title, a short description, and instructions for admin

    Attributes:
        title: A Streamlit title of the web.
        header: A Streamlit header of the web.
        info_field: A Streamlit reserved field,
            which contains short description of the web.
    """

    @staticmethod
    def welcome():
        """Sets up the welcome screen."""
        st.title("Wholesale Management System")
        st.header("Welcome to the WMS of company That Boring Company.")

    @staticmethod
    def intro():
        """Shows intro section."""
        st.markdown("""
            ---\n
            This is a project for Web Application Development course in
            [International University - VNU-HCM](https://hcmiu.edu.vn/en/).\n
            Source code is available at [GitHub](https://github.com/Doki064/WAD_IT093IU).
        """)

    @staticmethod
    def info():
        """Shows info, a short summary of intro section."""
        st.sidebar.markdown("""
            ---\n
            [International University - VNU-HCM](https://hcmiu.edu.vn/en/)\n
            [Streamlit](https://www.streamlit.io/)\n
            [GitHub](https://github.com/Doki064/WAD-IT093IU)
        """)

    @staticmethod
    async def form(state: SessionState, session: ClientSession):
        if state.form == "login":
            with st.form("login_form"):
                username = st.text_input("Username: ", value="", key="login_username")
                password = st.text_input("Password: ",
                                         type="password",
                                         value="",
                                         key="login_password")
                warn_msg = st.empty()
                submitted = st.form_submit_button("Sign in")
                if submitted and username and password:
                    response = await user.login(session, username, password)
                    if response.status != 200:
                        if response.status == 401:
                            warn_msg.warning("The username or password was not correct")
                        else:
                            st.error(response.status)
                            st.error(response.data["detail"])
                            st.stop()
                    state.token = response.data["access_token"]
                    st.experimental_rerun()

        else:
            with st.form("register_form"):
                username = st.text_input("Username: ", value="", key="register_username")
                uname_warn = st.empty()
                password = st.text_input("Password: ",
                                         type="password",
                                         value="",
                                         key="register_password")
                password_confirm = st.text_input("Confirm password: ",
                                                 type="password",
                                                 value="",
                                                 key="password_confirm")
                pwd_warn = st.empty()
                submitted = st.form_submit_button("Sign up")
                if submitted and username and password:
                    pattern = "^(?=.{8,20}$)(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._]+(?<![_.])$"
                    if re.match(pattern, username) is None:
                        uname_warn.warning("Username must be between 8 and 20 characters")
                        st.stop()
                    elif len(password) < 8 or len(password) > 30:
                        pwd_warn.warning("Password must be between 8 and 30 characters")
                        st.stop()
                    elif password_confirm != password:
                        pwd_warn.warning("The password confirmation does not match")
                        st.stop()
                    response = await user.register(session, username, password)
                    if response.status != 201:
                        st.error(response.status)
                        st.error(response.data["detail"])
                        st.stop()
                    state.token = response.data["access_token"]
                    st.experimental_rerun()
