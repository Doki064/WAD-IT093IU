import os

if os.getenv("NODE_ENV", "development") != "production":
    from pathlib import Path
    from dotenv import load_dotenv

    base_dir = Path(__file__).parents[1]
    load_dotenv(base_dir.joinpath(".env.local").resolve())

BASE_URL = os.getenv("BASE_URL")
API_PATH = os.getenv("API_PATH")

SERVER_URI = BASE_URL + API_PATH
