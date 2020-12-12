import atexit
import base64
import hashlib

import bcrypt
import streamlit as st

import SessionState
from src.gui.main_page import MainPage
from src.gui.menu import Menu

session_state = SessionState.get(password='')


def on_terminate():
    with open("src/encryption/check_session", "wb") as f:
        session_state.password = ""
        f.write(hashlib.sha1("IS_LOGGED_OUT".encode()).digest())


def login_section():
    st.sidebar.title("LOGIN SECTION")
    st.sidebar.write(""" 
        ## **WARNING: AUTHORIZED ACCESS ONLY**
        Input your administrator password on the left sidebar, then press "Enter" to login.
    """)
    input_password = st.sidebar.text_input("Input administrator password: ", type="password",
                                           value=session_state.password)
    return input_password


def main():
    atexit.register(on_terminate)

    with open("src/encryption/check_session", "rb+") as f:
        check_session = f.readline()
    with open("src/encryption/hash_pw", "rb") as f:
        hashed_password = f.read()

    st.set_page_config(page_title="Wholesale Management System", layout="wide")

    main_page = MainPage()
    main_page.call()

    if check_session != hashlib.sha1(str(session_state.session_id).encode()).digest():
        input_password = login_section()
        session_state.password = input_password

        if st.sidebar.button("Login") or input_password:
            if not bcrypt.checkpw(base64.b64encode(hashlib.sha256(session_state.password.encode()).digest()), hashed_password):
                st.sidebar.warning("Wrong password!")
                st.stop()
            else:
                with open("src/encryption/check_session", "wb") as f:
                    f.write(hashlib.sha1(str(session_state.session_id).encode()).digest())
                st.experimental_rerun()
    else:
        st.sidebar.title("Experimental App")
        if st.sidebar.button("Logout"):
            with open("src/encryption/check_session", "wb") as f:
                session_state.password = ""
                f.write(hashlib.sha1("IS_LOGGED_OUT".encode()).digest())
            st.experimental_rerun()
        menu = Menu()
        menu.display_option()
    st.sidebar.write("Note: this is a collapsible sidebar.")


if __name__ == "__main__":
    main()
