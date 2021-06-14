from settings import SERVER_HOST, SERVER_PORT

BASE_URL = f"http://{SERVER_HOST}:{SERVER_PORT}/api"


class Response:

    def __init__(self, status: int, data):
        self.status = status
        self.data = data
