from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from management import Management

import httpx
import pandas as pd
import streamlit as st

from api import customers


async def show_search(mngmt: Management):
    with st.beta_container():
        col1, col2 = st.beta_columns(2)
        with col1:
            st.info(
                """
                    Input id or name to search for customer in the database.
                    Default to search all customers.\n
                    *Limit to 1000 rows.*
                """
            )
            choice = st.radio("Search by all/id/name: ", options=["all", "id", "name"])

            if choice == "id":
                customer_id = st.number_input(
                    "Input customer id: ", step=1, value=0, min_value=0
                )
                response = await customers.get_by_id(mngmt.client, customer_id)
                try:
                    response.raise_for_status()
                except httpx.HTTPStatusError:
                    st.error(f"Status code: {response.status_code}")
                    st.error(response.json()["detail"])
                    st.stop()
                df = pd.json_normalize(response.json())

            elif choice == "name":
                customer_name = st.text_input("Input customer name: ", value="")
                response = await customers.get_by_name(mngmt.client, customer_name)
                try:
                    response.raise_for_status()
                except httpx.HTTPStatusError:
                    st.error(f"Status code: {response.status_code}")
                    st.error(response.json()["detail"])
                    st.stop()
                df = pd.json_normalize(response.json())

            else:
                response = await customers.get_all(mngmt.client, mngmt.limit)
                try:
                    response.raise_for_status()
                except httpx.HTTPStatusError:
                    st.error(f"Status code: {response.status_code}")
                    st.error(response.json()["detail"])
                    st.stop()
                df = pd.json_normalize(response.json())

            columns = st.multiselect(
                "Select columns to show: ", mngmt.self.tables["customers"]
            )

        with col2:
            with st.beta_expander("Show customer with selected column(s)", expanded=True):
                if not columns:
                    columns = mngmt.self.tables["customers"]
                st.dataframe(df[columns])
