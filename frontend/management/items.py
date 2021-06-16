from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from management import Management

import pandas as pd
import streamlit as st

from api import items


async def show_search(mngmt: Management):
    with st.beta_container():
        col1, col2 = st.beta_columns(2)
        with col1:
            st.info(
                """
                    Input id or name to search for item in the database.
                    Default to search all items.\n
                    *Limit to 1000 rows.*
                """
            )
            choice = st.radio("Search by all/id/name: ", options=["all", "id", "name"])

            if choice == "id":
                item_id = st.number_input("Input item id: ", step=1, value=0, min_value=0)
                response = await items.get_by_id(mngmt.client, item_id)
                if response.status != 200:
                    st.error(response.status)
                    st.error(response.data["detail"])
                    st.stop()
                df = pd.json_normalize(response.data)

            elif choice == "name":
                item_name = st.text_input("Input item name: ", value="")
                response = await items.get_by_name(mngmt.client, item_name)
                if response.status != 200:
                    st.error(response.status)
                    st.error(response.data["detail"])
                    st.stop()
                df = pd.json_normalize(response.data)

            else:
                response = await items.get_all(mngmt.client, mngmt.limit)
                if response.status != 200:
                    st.error(response.status)
                    st.error(response.data["detail"])
                    st.stop()
                df = pd.json_normalize(response.data)

            columns = st.multiselect(
                "Select columns to show: ", mngmt.self.tables["items"]
            )

        with col2:
            with st.beta_expander("Show item with selected column(s)", expanded=True):
                if not columns:
                    columns = mngmt.self.tables["items"]
                st.dataframe(df[columns])
