import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).absolute().parents[1]
load_dotenv(BASE_DIR.joinpath(".env"))

REQUEST_HOST = os.environ["REQUEST_HOST"]
REQUEST_PORT = os.environ["REQUEST_PORT"]
BASE_URL = f"http://{REQUEST_HOST}:{REQUEST_PORT}/api"


class Response:

    def __init__(self, status: int, data):
        self.status = status
        self.data = data
