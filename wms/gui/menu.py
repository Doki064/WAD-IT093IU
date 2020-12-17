"""
Example:
    >>> from wms import gui
    >>> menu_page = gui.Menu()
    >>> menu_page.display_option() # Display the select box
"""

import streamlit as st

from wms import sesson_state
from wms.gui._management import Management
from wms.gui._plot import Plot
from wms.gui._table import Table

state = sesson_state.get()


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

    def __init__(self, connection):
        """Initialize Menu instance."""
        self.container = st.sidebar.beta_container()
        self.options = ["Search", "Add", "Remove", "View table", "View profit plot"]
        self.management = Management(connection)
        self.plot = Plot(connection)
        self.table = Table(connection)

    def display_option(self):
        """Display options as select box"""

        # Options:
        #     'Search'            go to search page
        #     'Add'               go to add page
        #     'Remove'            go to remove page
        #     'View table'        view the statistics in the database
        #     'View profit plot'  view the plot of profit in a specific amount of time

        self.container.header("NAVIGATION")

        current_option = self.container.radio("Go to: ", self.options)
        if current_option == "Search":
            self.management.show_search()
        elif current_option == "Add":
            self.management.show_add()
        elif current_option == "Remove":
            self.management.show_remove()
        elif current_option == "View table":
            self.table.show_dataframe()
        elif current_option == "View profit plot":
            self.plot.plot()
        return self.container
