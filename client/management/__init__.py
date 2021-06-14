import streamlit as st
from aiohttp import ClientSession

from session_state import SessionState
from api import BASE_URL


class Management:

    @classmethod
    async def create(cls, state: SessionState, session: ClientSession):
        self = Management()
        self.state = state
        self.session = session
        self.limit = 1000
        self.current_option = ""
        async with self.session.get(f"{BASE_URL}/internal/admin/") as response:
            if response.status == 200:
                data = await response.json()
            else:
                st.error(response.status)
                err = await response.json()
                st.error(err["detail"])
                st.stop()
        self.tables = list(data.keys())
        try:
            self.tables.remove("importation_details")
            self.tables.remove("transaction_details")
        except ValueError:
            pass

    async def show(self):
        pass
