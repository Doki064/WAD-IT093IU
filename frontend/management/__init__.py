import httpx
import streamlit as st

from management import (
    customers,
    categories,
    items,
    shops,
    importations,
    transactions,
)
from session_state import SessionState


class Management:
    @classmethod
    async def create(cls, state: SessionState, client: httpx.AsyncClient):
        self = Management()
        self.state = state
        self.client = client
        self.limit = 1000
        self.metadata = None
        self.tables = None
        return self

    async def show_search(self):
        response = await self.client.get("/internal/admin")
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError:
            st.error(f"Status code: {response.status_code}")
            st.error(response.json()["detail"])
            st.stop()
        self.metadata = response.json()
        self.tables = list(self.metadata.keys())
        try:
            self.tables.remove("users")
            self.tables.remove("importation_details")
            self.tables.remove("transaction_details")
            self.state.mngmt_search = self.tables[0]
        except ValueError:
            pass

        self.state.mngmt_search = st.selectbox(
            "Select table to search: ",
            options=self.tables,
            index=self.tables.index(self.state.mngmt_search),
            key="mngmt_option_search"
        )
        await globals()[self.state.mngmt_search].show_search(self)
