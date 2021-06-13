import pandas as pd
import streamlit as st

from management import Management
from api import categories


async def show_category_search(mngmt: Management):
    with st.beta_container():
        col1, col2 = st.beta_columns(2)

        with col1:
            st.info("""
                    Input uid or name to search for category in the database.
                    Default to search all categories.\n
                    *Limit to 1000 rows.*
                """)
            choice = st.radio("Search by all/uid/name: ", options=["all", "uid", "name"])

            if choice == "uid":
                category_uid = st.number_input("Input category uid: ",
                                               step=1,
                                               value=0,
                                               min_value=0)
                response = await categories.get_by_uid(mngmt.session, category_uid)
                if response.status != 200:
                    st.error(response.status)
                    st.error(response.data["detail"])
                    st.stop()
                df = pd.json_normalize(response.data)

            elif choice == "name":
                category_name = st.text_input("Input category name: ", value="")
                response = await categories.get_by_name(mngmt.session, category_name)
                if response.status != 200:
                    st.error(response.status)
                    st.error(response.data["detail"])
                    st.stop()
                df = pd.json_normalize(response.data)
            else:
                response = await categories.get_all(mngmt.session, mngmt.limit)
                if response.status != 200:
                    st.error(response.status)
                    st.error(response.data["detail"])
                    st.stop()
                df = pd.json_normalize(response.data)

            columns = st.multiselect("Select columns to show: ",
                                     mngmt.self.tables["categories"])

        with col2:
            with st.beta_expander("Show category with selected column(s)", expanded=True):
                if not columns:
                    columns = mngmt.self.tables["categories"]
                st.dataframe(df[columns])
