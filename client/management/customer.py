import pandas as pd
import streamlit as st

from management import Management
from api import customers


async def show_customer_search(mngmt: Management):
    with st.beta_container():
        col1, col2 = st.beta_columns(2)
        with col1:
            st.info("""
                    Input uid or name to search for customer in the database.
                    Default to search all customers.\n
                    *Limit to 1000 rows.*
                """)
            choice = st.radio("Search by all/uid/name: ", options=["all", "uid", "name"])

            if choice == "id":
                customer_uid = st.number_input("Input customer uid: ",
                                               step=1,
                                               value=0,
                                               min_value=0)
                response = await customers.get_by_uid(mngmt.session, customer_uid)
                if response.status != 200:
                    st.error(response.status)
                    st.error(response.data["detail"])
                    st.stop()
                df = pd.json_normalize(response.data)

            elif choice == "name":
                customer_name = st.text_input("Input customer name: ", value="")
                response = await customers.get_by_name(mngmt.session, customer_name)
                if response.status != 200:
                    st.error(response.status)
                    st.error(response.data["detail"])
                    st.stop()
                df = pd.json_normalize(response.data)

            else:
                response = await customers.get_all(mngmt.session, mngmt.limit)
                if response.status != 200:
                    st.error(response.status)
                    st.error(response.data["detail"])
                    st.stop()
                df = pd.json_normalize(response.data)

            columns = st.multiselect("Select columns to show: ",
                                     mngmt.self.tables["customers"])

        with col2:
            with st.beta_expander("Show customer with selected column(s)", expanded=True):
                if not columns:
                    columns = mngmt.self.tables["customers"]
                st.dataframe(df[columns])