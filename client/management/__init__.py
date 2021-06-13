import os
from pathlib import Path

import streamlit as st
from aiohttp import ClientSession
from dotenv import load_dotenv

from session_state import SessionState

BASE_DIR = Path(__file__).absolute().parents[1]
load_dotenv(BASE_DIR.joinpath(".env"))

REQUEST_HOST = os.environ["REQUEST_HOST"]
REQUEST_PORT = os.environ["REQUEST_PORT"]
BASE_URL = f"http://{REQUEST_HOST}:{REQUEST_PORT}/api"


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
