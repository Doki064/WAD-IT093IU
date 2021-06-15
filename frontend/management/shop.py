import pandas as pd
import streamlit as st

from management import Management
from api import shops


async def show_shop_search(mngmt: Management):
    with st.beta_container():
        col1, col2 = st.beta_columns(2)
        with col1:
            st.info("""
                    Input id or name to search for shop in the database.
                    Default to search all shops.\n
                    *Limit to 1000 rows.*
                """)
            choice = st.radio("Search by all/id/name: ", options=["all", "id", "name"])

            if choice == "id":
                shop_id = st.number_input("Input item id: ", step=1, value=0, min_value=0)
                response = await shops.get_by_id(mngmt.session, shop_id)
                if response.status != 200:
                    st.error(response.status)
                    st.error(response.data["detail"])
                    st.stop()
                df = pd.json_normalize(response.data)

            elif choice == "name":
                shop_name = st.text_input("Input item name: ", value="")
                response = await shops.get_by_name(mngmt.session, shop_name)
                if response.status != 200:
                    st.error(response.status)
                    st.error(response.data["detail"])
                    st.stop()
                df = pd.json_normalize(response.data)

            else:
                response = await shops.get_all(mngmt.session, mngmt.limit)
                if response.status != 200:
                    st.error(response.status)
                    st.error(response.data["detail"])
                    st.stop()
                df = pd.json_normalize(response.data)

            columns = st.multiselect("Select columns to show: ",
                                     mngmt.self.tables["shops"])

        with col2:
            with st.beta_expander("Show shop with selected column(s)", expanded=True):
                if not columns:
                    columns = mngmt.self.tables["shops"]
                st.dataframe(df[columns])
