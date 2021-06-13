"""
Example:
    >>> import main_page
    >>> main_page = gui.MainPage()
    >>> gui.intro() # Display the intro section
    >>> gui.info() # Display the info on the sidebar
"""

import streamlit as st

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

    def __init__(self, state: SessionState):
        """Initializes MainPage instance."""
        self.state = state
        self.title = st.empty()
        self.header = st.empty()
        self.info_field = st.empty()

    def call(self):
        """Calls the welcome screen."""
        self._welcome()

    def _welcome(self):
        """Sets up the welcome screen."""
        self.title.title("Wholesale Management System")
        self.header.header("Welcome to the WMS of company That Boring Company.")

    @staticmethod
    def intro():
        """Shows intro section."""
        st.markdown("""
            ---\n
            This is a project for Web Application Development course in
            [International University - VNU-HCM](https://hcmiu.edu.vn/en/).\n
            The web application is built with [Streamlit](https://www.streamlit.io/).\n
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
