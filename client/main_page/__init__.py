"""
Example:
    >>> from wms import gui
    >>> main_page = gui.MainPage()
    >>> gui.intro() # Display the intro section
    >>> gui.info() # Display the info on the sidebar
"""

import streamlit as st


class MainPage:
    """Main Page of the Web App

    The main page displays the title, a short description, and instructions for admin

    Attributes:
        title: A Streamlit title of the web.
        header: A Streamlit header of the web.
        info_field: A Streamlit reserved field,
            which contains short description of the web.
    """

    def __init__(self):
        """Initializes MainPage instance."""
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


def intro():
    """Shows intro section."""
    st.markdown("""
        ---\n
        This is a wholesale management system project for Software Engineering course in
        [International University - VNU-HCM](https://hcmiu.edu.vn/en/).\n
        The web application is built with [Streamlit](https://www.streamlit.io/).\n
        Source code is available at [GitHub](https://github.com/minhlong94/SWE_IT076IU).\n
    """)


def info():
    """Shows info, a short summary of intro section."""
    st.sidebar.markdown("""
        ---\n
        [International University - VNU-HCM](https://hcmiu.edu.vn/en/)\n
        [Streamlit](https://www.streamlit.io/)\n
        [GitHub](https://github.com/minhlong94/SWE_IT076IU)\n
    """)
