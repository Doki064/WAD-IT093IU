import os
from time import sleep

import streamlit as st

import wms
from wms import cli
from wms import database
from wms import encryption
from wms import gui
from wms import sesson_state


@st.cache(allow_output_mutation=True, show_spinner=False, max_entries=1, ttl=300)
def _get_cached_id():
    return dict()


def run(**kwargs):
    try:
        state = sesson_state.get()

        if kwargs.get("demo") is True:
            security_key = os.path.join(os.path.dirname(wms.__file__), "hello/dummy/.security_key")
            database_file = os.path.join(os.path.dirname(wms.__file__), "hello/dummy/wms.db")
            csv_zip = os.path.join(os.path.dirname(wms.__file__), "hello/dummy/dummy_data.zip")
        else:
            security_key = cli.SECURITY_KEY
            database_file = cli.DATABASE_FILE
            csv_zip = None

        st.set_page_config(page_title="Wholesale Management System", layout="wide")
        connection = database.create_connection(db_file=database_file, csv_zip=csv_zip)

        main_page = gui.MainPage()
        main_page.call()

        if not os.path.exists(security_key):
            gui.intro()

            st.info("This is the first time you have run this application, please create a new security key first.")
            st.subheader("NEW SECURITY KEY")

            state.key = st.text_input("Input your new security key: ", type="password",
                                      value=state.key or "")
            state.confirm_key = st.text_input("Confirm your security key: ", type="password",
                                              value=state.confirm_key or "")

            if st.button("Register") and state.key and state.confirm_key:
                if len(state.key) < 6:
                    with st.error("Your security key must be at least 6 characters."):
                        sleep(1)
                        state.clear()
                elif state.key != state.confirm_key:
                    with st.error("Your confirmation key does not match."):
                        sleep(1)
                        state.clear()
                else:
                    encryption.hash_password(security_key, state.key)
                    state.clear()

        elif not state.is_login:
            gui.intro()

            st.sidebar.header("LOGIN SECTION")
            st.sidebar.subheader("**WARNING: AUTHORIZED ACCESS ONLY**")
            st.sidebar.write("""
                Enter your privileged password on this sidebar, then click **Sign in** to login.
            """)

            state.login_key = st.sidebar.text_input("Enter the privileged password: ", type="password",
                                                    value=state.encryption_key or "",
                                                    key="login_section")

            if st.sidebar.button("Sign in"):
                if not encryption.check_password(security_key, state.login_key):
                    with st.sidebar.warning("Wrong password!"):
                        sleep(1)
                        state.clear()
                else:
                    state.remove('login_key')
                    state.is_login = True
                    st.experimental_rerun()

        else:
            st.sidebar.header("LOGOUT SECTION")
            st.sidebar.write(f"*Current session ID: {state.get_id()}*")
            state.logout_key = st.sidebar.text_input("Enter the privileged password: ", type="password",
                                                     value=state.logout_key or "",
                                                     key="logout_section")
            if st.sidebar.button("Sign out"):
                if not encryption.check_password(security_key, state.logout_key):
                    with st.sidebar.warning("Wrong password!"):
                        sleep(1)
                        st.experimental_rerun()
                else:
                    state.clear()

            menu = gui.Menu(connection)
            menu.display_option()

            gui.info()

        state.sync()

    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    run(demo=True)
