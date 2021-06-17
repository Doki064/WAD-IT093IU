"""
Example:
    >>> from wms import gui
    >>> menu_page = gui.Menu()
    >>> menu_page.display_option() # Display the select box
"""

import streamlit as st
from httpx import AsyncClient

from management import Management as _Management
from plot import Plot as _Plot
from table import Table as _Table
from session_state import SessionState


class Menu:
    """Menu

    Page that appears after successfully login. Includes a select box to ask user options.

    Attributes:
        container: A Streamlit container to place its widgets.
        options: A list of string storing the options of the menu.
        management: An instance of Management to handle database APIs.
        plot: An instance of Plot to show the plot of profit.
        table: An instance of Table to display data statistics of the database.
    """
    @classmethod
    async def create(cls, state: SessionState, client: AsyncClient):
        """Initialize Menu instance."""
        self = Menu()
        self.state = state
        self.client = client
        self.container = st.sidebar.beta_container()
        self.options = ["Search", "Add", "Remove", "View table", "View plot"]
        self.management = await _Management.create(state, client)
        self.table = _Table(state, client)
        self.plot = await _Plot.create(state, client)
        return self

    async def display_option(self):
        """Display options as select box"""

        # Options:
        #     'Search'            go to search page
        #     'Add'               go to add page
        #     'Remove'            go to remove page
        #     'View table'        view the statistics in the database
        #     'View plot'         view the plot of profit in a specific amount of time

        self.container.header("NAVIGATION")

        current_option = self.container.radio("Go to: ", self.options)
        if current_option == "Search":
            await self.management.show_search()
        if current_option == "Add":
            st.warning("Not implemented")
            st.stop()
        if current_option == "Remove":
            st.warning("Not implemented")
            st.stop()
        if current_option == "View table":
            await self.table.show_dataframe()
        if current_option == "View plot":
            await self.plot.plot()
        return self.container
