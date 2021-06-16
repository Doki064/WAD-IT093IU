import streamlit as st

from management import (
    customers,
    categories,
    items,
    shops,
    importations,
    transactions,
)
from core.config import SERVER_URI


class Management:
    @classmethod
    async def create(cls, state, client):
        self = Management()
        self.state = state
        self.client = client
        self.limit = 1000
        async with self.client.get(f"{SERVER_URI}/internal/admin/") as response:
            if response.status >= 400:
                st.error(response.status)
                err = await response.json()
                st.error(err["detail"])
                st.stop()
            data = await response.json()
        self.tables = list(data.keys())
        try:
            self.tables.remove("users")
            self.tables.remove("importation_details")
            self.tables.remove("transaction_details")
            self.state.mngmt_search = self.tables[0]
        except ValueError:
            pass
        return self

    async def show_search(self):
        self.state.mngmt_search = st.selectbox(
            "Select table to search: ",
            options=self.tables,
            index=self.tables.index(self.state.mngmt_search),
            key="mngmt_option_search"
        )
        await globals()[self.state.mngmt_search].show_search(self)
