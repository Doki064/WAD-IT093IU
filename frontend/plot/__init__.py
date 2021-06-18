"""
Example:
    >>> from wms.gui._plot import Plot
    >>> plot = Plot()
    >>> plot.plot()
"""

import io
from datetime import datetime, date
from typing import List

import httpx
import pandas as pd
import streamlit as st

from api.transactions import get_min_max_dates
from session_state import SessionState


class Plot:
    """Plot the profit

    Attributes:
        df: pandas DataFrame. The sales DF.
        shop_df: pandas DataFrame. The mapping from shop_id to shop_name
        min_date = datetime.datetime. The min date in the sales df
        max_date: datetime.datetime. The max date in the sales df
        shop_ids: list of int. List of shop ids
        num_days_to_plot_week: int, default 90.
            If days between start_date and end_date <90, do weekly plot, else monthly plot
        template: string, default "ggplot2". Plotly.express template.
    """
    @classmethod
    async def create(cls, state: SessionState, client: httpx.AsyncClient):
        self = Plot()
        self.state = state
        self.client = client
        self.df = None
        self.profit_df = None
        self.shop_df = None
        self.min_date = None
        self.max_date = None
        self.shop_ids = None
        self.datetime_format = "%Y-%m-%d"
        self.num_days_to_plot_week = 90
        self.template = "plotly"
        return self

    async def plot(self):
        """Plot the profit

        Get user's inputs: `start_date`, `end_date` and `shop_id`.\n
        Check if `end_date` >= `start_date`, raises `AssertionError` if False.\n
        Select in the DF that is between `start_date` and `end_date`
            and only contains `shop_id`.\n
        Group the selected DF by week or month depends on the condition,
            then use `plotly.express` to plot the line chart.

        Raises:
            AssertionError: if `end_date` is less than `start_date`
        """
        if self.state.plot is None:
            self.state.plot = {}

        response = await get_min_max_dates(self.client)
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError:
            st.error(f"Status code: {response.status_code}")
            st.error(response.json()["detail"])
            st.stop()
        date_range = response.json()
        self.min_date = date.fromisoformat(date_range["min_date"])
        self.max_date = date.fromisoformat(date_range["max_date"])

        # self.df = await _load_df(self.client)
        self.shop_df = await _load_shop(self.client)

        # self.min_date = self.df["date"].min()
        # self.max_date = self.df["date"].max()
        self.shop_ids = tuple(self.shop_df["id"].unique())

        with st.beta_container():
            st.info(
                """
                Please choose the start date and end date.
                Please note that start day should be less than end date.
                """
            )
            self.state.plot["start_date"] = datetime.fromordinal(
                st.date_input(
                    "Start date",
                    value=self.state.plot.get("start_date", None) or self.min_date,
                    min_value=self.min_date,
                    max_value=self.max_date,
                    key="start"
                ).toordinal()
            )
            self.state.plot["end_date"] = datetime.fromordinal(
                st.date_input(
                    "End date",
                    value=self.state.plot.get("end_date", None) or self.max_date,
                    min_value=self.min_date,
                    max_value=self.max_date,
                    key="end"
                ).toordinal()
            )
            shop_ids = st.multiselect("Select the SHOP ID: ", self.shop_ids)

            button = st.button("Get plot")

        col1, col2 = st.beta_columns(2)
        with col1:
            st.write("#### All shops with their ids")
            st.dataframe(self.shop_df)

        try:
            self.state.plot["start_date"]
            self.state.plot["end_date"]
        except KeyError:
            st.stop()

        with col2:
            if self.state.plot.get("fig", None) is not None:
                fig = self.state.plot["fig"]
                st.plotly_chart(fig, use_container_width=True)
            if button:
                # Sanity check start_date and end_date
                if self.state.plot["start_date"] > self.state.plot["end_date"]:
                    st.warning("Start date must be before end date.")
                    st.stop()
                self.state.plot["fig"] = None

                fig = await _load_df(
                    self.client, self.state.plot["start_date"].date(),
                    self.state.plot["end_date"].date(), shop_ids
                )
                self.state.plot["fig"] = fig


async def _load_df(
    client: httpx.AsyncClient,
    start_date: date,
    end_date: date,
    shop_ids: List[int],
    skip: int = 0,
    limit: int = 1000000
):
    params = {
        "start_date": start_date,
        "end_date": end_date,
        "shop_ids": shop_ids,
        "skip": skip,
        "limit": limit,
    }
    response = await client.get("/internal/admin/plot", params=params, timeout=None)
    try:
        response.raise_for_status()
    except httpx.HTTPStatusError:
        st.error(f"Status code: {response.status_code}")
        st.error(response.json()["detail"])
        st.stop()
    return response.json()


async def _load_shop(client: httpx.AsyncClient):
    response = await client.get("/shops", timeout=None)
    try:
        response.raise_for_status()
    except httpx.HTTPStatusError:
        st.error(f"Status code: {response.status_code}")
        st.error(response.json()["detail"])
        st.stop()
    df = pd.json_normalize(response.json())
    return df
