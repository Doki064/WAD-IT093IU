from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from management import Management

import httpx
import pandas as pd
import streamlit as st

from api import categories


async def show_search(mngmt: Management):
    with st.beta_container():
        st.info(
            """
                Input id or name to search for category in the database.
                Default to search all categories.\n
                *Limit to 1000 rows.*
            """
        )
        col1, col2 = st.beta_columns(2)
        with col1:
            choice = st.radio("Search by all/id/name: ", options=["all", "id", "name"])

            if choice == "id":
                category_id = st.number_input(
                    "Input category id: ", step=1, value=0, min_value=0
                )
                if not category_id:
                    st.stop()
                response = await categories.get_by_id(mngmt.client, category_id)
                try:
                    response.raise_for_status()
                except httpx.HTTPStatusError:
                    st.error(f"Status code: {response.status_code}")
                    st.error(response.json()["detail"])
                    st.stop()
                df = pd.json_normalize(response.json())

            elif choice == "name":
                category_name = st.text_input("Input category name: ", value="")
                if not category_name:
                    st.stop()
                response = await categories.get_by_name(mngmt.client, category_name)
                try:
                    response.raise_for_status()
                except httpx.HTTPStatusError:
                    st.error(f"Status code: {response.status_code}")
                    st.error(response.json()["detail"])
                    st.stop()
                df = pd.json_normalize(response.json())

            else:
                response = await categories.get_all(mngmt.client, limit=mngmt.limit)
                try:
                    response.raise_for_status()
                except httpx.HTTPStatusError:
                    st.error(f"Status code: {response.status_code}")
                    st.error(response.json()["detail"])
                    st.stop()
                df = pd.json_normalize(response.json())

            columns = st.multiselect(
                "Select columns to show: ", mngmt.metadata["categories"]
            )

        with col2:
            with st.beta_expander("Show category with selected column(s)", expanded=True):
                if not columns:
                    columns = mngmt.metadata["categories"]
                st.dataframe(df[columns])
