from core.config import SERVER_URI

BASE_URL = SERVER_URI


class Response:

    def __init__(self, status: int, data):
        self.status = status
        self.data = data
