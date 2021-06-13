import pandas as pd
import streamlit as st

from management import Management
from api import transactions


async def show_transaction_search(mngmt: Management):
    with st.beta_container():
        st.info("""
                Input uid or date to search for transaction in the database.
                Default to search all transactions.\n
                *Limit to 1000 rows.*
            """)
        choice = st.radio("Search by all/uid/date: ", options=["all", "uid"])

        if choice == "id":
            transaction_uid = st.number_input("Input transaction uid: ",
                                              step=1,
                                              value=0,
                                              min_value=0)
            response = await transactions.get_by_uid(mngmt.session, transaction_uid)
            if response.status != 200:
                st.error(response.status)
                st.error(response.data["detail"])
                st.stop()
            df = pd.json_normalize(response.data)

        elif choice == "date":
            transaction_date = st.date_input("Input transaction date: ")
            response = await transactions.get_by_date(mngmt.session, transaction_date)
            if response.status != 200:
                st.error(response.status)
                st.error(response.data["detail"])
                st.stop()
            df = pd.json_normalize(response.data)

        else:
            response = await transactions.get_all(mngmt.session, mngmt.limit)
            if response.status != 200:
                st.error(response.status)
                st.error(response.data["detail"])
                st.stop()
            df = pd.json_normalize(response.data)

        columns = st.multiselect("Select columns to show: ",
                                 mngmt.self.tables["transactions"])

        col1, col2 = st.beta_columns(2)
        with col1:
            with st.beta_expander("Show transaction with selected column(s)",
                                  expanded=True):
                if not columns:
                    columns = mngmt.self.tables["transactions"]
                st.dataframe(df[columns])
        with col2:
            with st.beta_expander("Show transaction details", expanded=True):
                uid_list = df["uid"].tolist()
                if len(uid_list) == 1:
                    uid = uid_list[0]
                else:
                    uid = st.selectbox("Select transaction: ", options=uid_list)

                response = await transactions.get_details(mngmt.session, uid)
                if response.status != 200:
                    st.error(response.status)
                    st.error(response.data["detail"])
                    st.stop()
                detail_df = pd.json_normalize(response.data)
                st.dataframe(detail_df)
