"""
Example:
    >>> from wms.gui._plot import Plot
    >>> plot = Plot()
    >>> plot.plot()
"""

from datetime import datetime

import pandas as pd
import plotly.express as px
import streamlit as st
from httpx import AsyncClient

from session_state import SessionState
from core.config import SERVER_URI


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
    async def create(cls, state: SessionState, client: AsyncClient):
        self = Plot()
        self.state = state
        self.client = client
        self.df = await _load_df(self.client)
        self.shop_df = await _load_shop(self.client)
        self.min_date = self.df["date"].min()
        self.max_date = self.df["date"].max()
        self.shop_ids = tuple(self.shop_df["id"].unique())
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

        with st.beta_container():
            # Options
            st.info(
                """
                Please choose the start date and end date.
                Please note that start day should be less than end date.
            """
            )
            self.state.plot["start_date"] = datetime.fromordinal(
                st.date_input(
                    "Start date",
                    value=self.min_date,
                    min_value=self.min_date,
                    max_value=self.max_date,
                    key="start"
                ).toordinal()
            )
            self.state.plot["end_date"] = datetime.fromordinal(
                st.date_input(
                    "End date",
                    value=self.max_date,
                    min_value=self.min_date,
                    max_value=self.max_date,
                    key="end"
                ).toordinal()
            )
            self.state.plot["shop_ids"] = st.multiselect(
                "Select the SHOP ID: ",
                self.shop_ids,
                default=self.state.plot.get("shop_ids", None)
            )

        col1, col2 = st.beta_columns(2)
        with col1:
            with st.beta_expander("Show shop"):
                st.dataframe(self.shop_df)    # Show the sample DF

        try:
            assert self.state.plot.get("start_date", None) is not None
            assert self.state.plot.get("end_date", None) is not None
            assert self.state.plot.get("shop_ids", None) is not None
        except AssertionError:
            st.stop()

        # Sanity check start_date and end_date
        try:
            assert self.state.plot["start_date"] <= self.state.plot["end_date"]
        except AssertionError:
            st.warning("Start date must be before end date.")
        else:
            # Get days in between
            days_in_between = self.state.plot["end_date"] - self.state.plot["start_date"]

            selected_df = _select_df_in_between(
                self.df, self.state.plot["start_date"], self.state.plot["end_date"],
                self.state.plot["shop_ids"]
            )
            plot_title = " profit of shop {} from {} to {}".format(
                self.state.plot["shop_ids"], self.state.plot["start_date"].date(),
                self.state.plot["end_date"].date()
            )
            with col2:
                with st.beta_expander("Show chart"):
                    if not self.state.plot["shop_ids"]:
                        st.warning("Please choose at least one shop id first.")
                        fig = px.line(
                            title="A beautiful blank chart", template=self.template
                        )
                    elif days_in_between.days <= self.num_days_to_plot_week:
                        st.info("Plotting profit by week")
                        profit_df = _group_by(selected_df, "W-MON")
                        st.dataframe(profit_df)
                        fig = px.line(
                            profit_df,
                            x="date",
                            y="profit",
                            title="Weekly" + plot_title,
                            template=self.template
                        )    # Plotly line chart
                    else:
                        st.info("Plotting profit by month")
                        profit_df = _group_by(selected_df, "M")
                        fig = px.line(
                            profit_df,
                            x="date",
                            y="profit",
                            title="Monthly" + plot_title,
                            template=self.template,
                            color="shopID"
                        )    # Plotly
                    fig.update_layout(title_x=0.5)
                    st.plotly_chart(fig, use_container_width=True)


@st.cache(persist=True, show_spinner=False)
async def _load_df(client: AsyncClient):
    # query = '''
    #         SELECT t.transactionDate, t.shopID, td.itemID,
    #             td.itemPrice, td.transactionAmount
    #         FROM Transactions t INNER JOIN TransactionDetail td
    #         ON t.transactionID = td.transactionID
    #         '''
    response = await client.get(f"{SERVER_URI}/transactions")
    assert response.raise_for_status() is None
    df = pd.json_normalize(response.json())
    df = df[["date", "shop_id", "item_id", "item_price", "item_amount"]]
    df["date"] = pd.to_datetime(df["date"])
    return df


@st.cache(persist=True, show_spinner=False)
async def _load_shop(client: AsyncClient):
    response = await client.get(f"{SERVER_URI}/shops")
    assert response.raise_for_status() is None
    df = pd.json_normalize(response.json())
    return df


@st.cache(show_spinner=False)
def _select_df_in_between(df, start_date, end_date, shop_ids):
    """Get subset of DF that is between given dates

    Arguments:
         df: pandas DataFrame.
         start_date (datetime): The start date to select
         end_date (datetime): The end date to select. `start_date` <= `end_date`
         shop_ids (int): The shop id to select
    Returns:
        selected_df: pandas DataFrame. Subset of the DF with the given condition
    """

    selected_df = df[(df["date"].between(start_date, end_date)) &
                     (df["shop_id"].isin(shop_ids))]
    # selected_df["profit"] = selected_df["itemPrice"] * selected_df["transactionAmount"]
    selected_df.loc[:, "profit"] = selected_df.loc[:, "item_price"].multiply(
        selected_df.loc[:, "item_amount"], axis="index"
    )
    return selected_df


@st.cache(show_spinner=False)
def _group_by(df, freq):
    """Group DF by freq

    Arguments:
        df: pandas DataFrame. The DF that needs to group by column "date"
        freq: string. Either "W-MON" (weekly group) or "M" (monthly group)

    Returns:
         profit_df: pandas DataFrame. The grouped DF by freq, with profit calculated.
    """
    df["date"] = pd.to_datetime(df["date"]) - pd.to_timedelta(7, unit="d")
    profit_df = df.groupby([pd.Grouper(key="date", freq=freq), "shop_id"])["profit"] \
        .sum() \
        .reset_index() \
        .sort_values("date")  # Group by week
    return profit_df
