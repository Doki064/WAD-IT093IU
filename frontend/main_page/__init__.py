"""
Example:
    >>> import main_page
    >>> main_page = gui.MainPage()
    >>> gui.intro() # Display the intro section
    >>> gui.info() # Display the info on the sidebar
"""

import re

import httpx
import streamlit as st

from api import user
from session_state import SessionState


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
        st.markdown(
            """
            ---\n
            This is a project for Web Application Development course in
            [International University - VNU-HCM](https://hcmiu.edu.vn/en/).\n
            Source code is available at [GitHub](https://github.com/Doki064/WAD-IT093IU).
        """
        )

    @staticmethod
    def info():
        """Shows info, a short summary of intro section."""
        st.sidebar.markdown(
            """
            ---\n
            [International University - VNU-HCM](https://hcmiu.edu.vn/en/)\n
            [GitHub](https://github.com/Doki064/WAD-IT093IU)
        """
        )

    @staticmethod
    async def form(state: SessionState, client: httpx.AsyncClient):
        if state.form == "login":
            with st.form("login_form"):
                username = st.text_input("Username: ", value="", key="login_username")
                password = st.text_input(
                    "Password: ", type="password", value="", key="login_password"
                )
                submitted = st.form_submit_button("Sign in")
                if submitted and username and password:
                    response = await user.login(client, username, password)
                    try:
                        response.raise_for_status()
                    except httpx.HTTPStatusError:
                        st.error(f"Status code: {response.status_code}")
                        st.error(response.json()["detail"])
                        st.stop()
                    return response.json()
        else:
            with st.form("register_form"):
                username = st.text_input("Username: ", value="", key="register_username")
                uname_warn = st.empty()
                password = st.text_input(
                    "Password: ", type="password", value="", key="register_password"
                )
                password_confirm = st.text_input(
                    "Confirm password: ",
                    type="password",
                    value="",
                    key="password_confirm"
                )
                pwd_warn = st.empty()
                submitted = st.form_submit_button("Sign up")
                if submitted and username and password:
                    pattern = "^(?=.{8,20}$)(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._]+(?<![_.])$"
                    if re.match(pattern, username) is None:
                        uname_warn.warning(
                            "Username can only contain letters and numbers and must be between 8 and 20 characters"    # noqa: E501
                        )
                        st.stop()
                    elif len(password) < 8 or len(password) > 30:
                        pwd_warn.warning("Password must be between 8 and 30 characters")
                        st.stop()
                    elif password_confirm != password:
                        pwd_warn.warning("The password confirmation does not match")
                        st.stop()
                    response = await user.register(client, username, password)
                    try:
                        response.raise_for_status()
                    except httpx.HTTPStatusError:
                        st.error(f"Status code: {response.status_code}")
                        st.error(response.json()["detail"])
                        st.stop()
                    return response.json()
