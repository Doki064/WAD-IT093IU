import streamlit as st
from httpx import AsyncClient

from management import (
    customers,
    categories,
    items,
    shops,
    importations,
    transactions,
)
from session_state import SessionState
from core.config import SERVER_URI


class Management:
    @classmethod
    async def create(cls, state: SessionState, client: AsyncClient):
        self = Management()
        self.state = state
        self.client = client
        self.limit = 1000
        self.tables = None
        return self

    async def show_search(self):
        response = await self.client.get(f"{SERVER_URI}/internal/admin/")
        if response.raise_for_status() is None:
            data = response.json()
        self.tables = list(data.keys())
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
