from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from management import Management

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
        choice = st.radio("Search by all/id/date: ", options=["all", "id"])

        if choice == "id":
            transaction_id = st.number_input(
                "Input transaction id: ", step=1, value=0, min_value=0
            )
            response = await transactions.get_by_id(mngmt.client, transaction_id)
            if response.status != 200:
                st.error(response.status)
                st.error(response.data["detail"])
                st.stop()
            df = pd.json_normalize(response.data)

        elif choice == "date":
            transaction_date = st.date_input("Input transaction date: ")
            response = await transactions.get_by_date(mngmt.client, transaction_date)
            if response.status != 200:
                st.error(response.status)
                st.error(response.data["detail"])
                st.stop()
            df = pd.json_normalize(response.data)

        else:
            response = await transactions.get_all(mngmt.client, mngmt.limit)
            if response.status != 200:
                st.error(response.status)
                st.error(response.data["detail"])
                st.stop()
            df = pd.json_normalize(response.data)

        columns = st.multiselect(
            "Select columns to show: ", mngmt.self.tables["transactions"]
        )

        col1, col2 = st.beta_columns(2)
        with col1:
            with st.beta_expander(
                "Show transaction with selected column(s)", expanded=True
            ):
                if not columns:
                    columns = mngmt.self.tables["transactions"]
                st.dataframe(df[columns])
        with col2:
            with st.beta_expander("Show transaction details", expanded=True):
                id_list = df["id"].tolist()
                if len(id_list) == 1:
                    id = id_list[0]
                else:
                    id = st.selectbox("Select transaction: ", options=id_list)

                response = await transactions.get_details(mngmt.client, id)
                if response.status != 200:
                    st.error(response.status)
                    st.error(response.data["detail"])
                    st.stop()
                detail_df = pd.json_normalize(response.data)
                st.dataframe(detail_df)
