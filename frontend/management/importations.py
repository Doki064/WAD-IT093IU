from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from management import Management

import httpx
import pandas as pd
import streamlit as st

from api import importations


async def show_search(mngmt: Management):
    with st.beta_container():
        st.info(
            """
                Input id or date to search for importation in the database.
                Default to search all importations.\n
                *Limit to 1000 rows.*
            """
        )
        choice = st.radio("Search by all/id/date: ", options=["all", "id"])

        if choice == "id":
            importation_id = st.number_input(
                "Input importation id: ", step=1, value=0, min_value=0
            )
            response = await importations.get_by_id(mngmt.client, importation_id)
            try:
                response.raise_for_status()
            except httpx.HTTPStatusError:
                st.error(f"Status code: {response.status_code}")
                st.error(response.json()["detail"])
                st.stop()
            df = pd.json_normalize(response.json())

        elif choice == "date":
            importation_date = st.date_input("Input importation date: ")
            response = await importations.get_by_date(mngmt.client, importation_date)
            try:
                response.raise_for_status()
            except httpx.HTTPStatusError:
                st.error(f"Status code: {response.status_code}")
                st.error(response.json()["detail"])
                st.stop()
            df = pd.json_normalize(response.json())

        else:
            response = await importations.get_all(mngmt.client, mngmt.limit)
            try:
                response.raise_for_status()
            except httpx.HTTPStatusError:
                st.error(f"Status code: {response.status_code}")
                st.error(response.json()["detail"])
                st.stop()
            df = pd.json_normalize(response.json())

        columns = st.multiselect(
            "Select columns to show: ", mngmt.self.tables["importations"]
        )

        col1, col2 = st.beta_columns(2)
        with col1:
            with st.beta_expander(
                "Show importation with selected column(s)", expanded=True
            ):
                if not columns:
                    columns = mngmt.self.tables["importations"]
                st.dataframe(df[columns])
        with col2:
            with st.beta_expander("Show importation details", expanded=True):
                id_list = df["id"].tolist()
                if len(id_list) == 1:
                    id = id_list[0]
                else:
                    id = st.selectbox("Select importation: ", options=id_list)

                response = await importations.get_details(mngmt.client, id)
                try:
                    response.raise_for_status()
                except httpx.HTTPStatusError:
                    st.error(f"Status code: {response.status_code}")
                    st.error(response.json()["detail"])
                    st.stop()
                detail_df = pd.json_normalize(response.json())
                st.dataframe(detail_df)
