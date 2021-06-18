from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from management import Management

from datetime import date

import httpx
import pandas as pd
import streamlit as st

from api import transactions


async def show_search(mngmt: Management):
    with st.beta_container():
        st.info(
            """
                Input id or date to search for transaction in the database.
                Default to search all transactions.\n
                *Limit to 1000 rows.*
            """
        )
        col1, col2 = st.beta_columns(2)
        with col1:
            choice = st.radio("Search by all/id/date: ", options=["all", "id", "date"])

            if choice == "id":
                transaction_id = st.number_input(
                    "Input transaction id: ", step=1, value=0, min_value=0
                )
                if not transaction_id:
                    st.stop()
                response = await transactions.get_by_id(mngmt.client, transaction_id)
                try:
                    response.raise_for_status()
                except httpx.HTTPStatusError:
                    st.error(f"Status code: {response.status_code}")
                    st.error(response.json()["detail"])
                    st.stop()
                df = pd.json_normalize(response.json())

            elif choice == "date":
                response = await transactions.get_min_max_dates(mngmt.client)
                try:
                    response.raise_for_status()
                except httpx.HTTPStatusError:
                    st.error(f"Status code: {response.status_code}")
                    st.error(response.json()["detail"])
                    st.stop()
                date_range = response.json()
                min_date = date.fromisoformat(date_range["min_date"])
                max_date = date.fromisoformat(date_range["max_date"])
                st.info(f"Min date: {min_date} | Max date: {max_date}")
                transaction_date = st.date_input(
                    "Input transaction date: ",
                    value=min_date,
                    min_value=min_date,
                    max_value=max_date
                )
                if not transaction_date:
                    st.stop()
                response = await transactions.get_by_date(mngmt.client, transaction_date)
                try:
                    response.raise_for_status()
                except httpx.HTTPStatusError:
                    st.error(f"Status code: {response.status_code}")
                    st.error(response.json()["detail"])
                    st.stop()
                df = pd.json_normalize(response.json())

            else:
                response = await transactions.get_all(mngmt.client, limit=mngmt.limit)
                try:
                    response.raise_for_status()
                except httpx.HTTPStatusError:
                    st.error(f"Status code: {response.status_code}")
                    st.error(response.json()["detail"])
                    st.stop()
                df = pd.json_normalize(response.json())

            columns = st.multiselect(
                "Select columns to show: ", mngmt.metadata["transactions"]
            )

        with col2:
            with st.beta_expander(
                "Show transaction with selected column(s)", expanded=True
            ):
                if not columns:
                    columns = mngmt.metadata["transactions"]
                st.dataframe(df[columns])
            with st.beta_expander("Show transaction details", expanded=True):
                id_list = df["id"].tolist()
                if len(id_list) == 1:
                    id = id_list[0]
                else:
                    id = st.selectbox("Select transaction: ", options=id_list)

                response = await transactions.get_details(mngmt.client, id)
                try:
                    response.raise_for_status()
                except httpx.HTTPStatusError:
                    st.error(f"Status code: {response.status_code}")
                    st.error(response.json()["detail"])
                    st.stop()
                detail_df = pd.json_normalize(response.json())
                st.dataframe(detail_df)
