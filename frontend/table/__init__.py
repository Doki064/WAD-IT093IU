"""
Example:
    >>> from table import Table
    >>> table = Table()
    >>> table.show_dataframe() # Show options and the selected DataFrame
"""

import io

import hiplot as hip
import pandas as pd
import pandas_profiling as pp
import streamlit as st
import streamlit.components.v1 as components
from aiohttp import ClientSession

from session_state import SessionState
from api import BASE_URL


class Table:
    """Table displayer

    Display the top few rows of the table (DataFrame),
        its information and the Pandas Profiling HTML.

    Attributes:
        show_df: pandas DataFrame. DataFrame that will be displayed. Limit to 200 rows.
        profile_df: pandas DataFrame.
            DataFrame that will be calculated using Pandas Profiling.
            This DF is usually the full DataFrame.
        limit_rows: int, default 200. Number of rows to be displayed as sample
        select_box: streamlit container.
            A select box to ask admin which DataFrame to display.
        dataframe: streamlit container. A container to display the DataFrame.
        text: string. The instruction for admin.
        profile_report: Pandas Profiling ProfileReport.
            The Pandas Profiling ProfileReport that will be displayed as HTML.
    """

    def __init__(self, state: SessionState, session: ClientSession):
        """Initializes Table instance."""
        self.state = state
        self.session = session
        self.show_df = None
        self.profile_df = None
        self.limit_rows = 100000
        self.select_box = st.empty()
        self.dataframe = st.empty()
        self.text = ("Choose the DataFrame (table) you want to display. "
                     "The viewer is limited to {} rows.".format(self.limit_rows))
        self.profile_report = None

    async def show_dataframe(self, minimal=True):
        with st.beta_container():
            # Options
            async with self.session.get(f"{BASE_URL}/internal/admin/") as response:
                if response.status == 200:
                    data = await response.json()
                else:
                    st.error(response.status)
                    err = await response.json()
                    st.error(err["detail"])
                    st.stop()
            options = tuple(data.keys())
            table = st.selectbox(self.text, options, index=3)
            st.info(f"Note: due to limited output size, the displayed DataFrame is "
                    f"limited to the first {self.limit_rows} rows only.\n\n"
                    f"However, the Pandas Profiling Report "
                    f"calculates on the full DataFrame.")

            col1, col2 = st.beta_columns(2)
            with col1:
                async with self.session.get(f"{BASE_URL}/{table}/") as response:
                    if response.status == 200:
                        data = await response.json()
                    else:
                        st.error(response.status)
                        err = await response.json()
                        st.error(err["detail"])
                        st.stop()
                df = pd.json_normalize(data)
                self.show_df = df.head(self.limit_rows)    # Only shows limited rows
                self.profile_df = df

                # Show DataFrame's info
                buffer = io.StringIO()
                df.info(buf=buffer)
                st.text(buffer.getvalue())

                # Show HiPlot
                xp = hip.Experiment.from_dataframe(self.show_df)
                xp.display_st(key="hip")

            with col2:
                # Show Pandas Profile Report
                self.profile_report = pp.ProfileReport(self.profile_df,
                                                       minimal=minimal,
                                                       progress_bar=False)
                with st.spinner("Generating profile report..."):
                    components.html(self.profile_report.to_html(),
                                    height=1500,
                                    scrolling=True)
