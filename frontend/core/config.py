import os

if os.getenv("PYTHON_ENV", "development") != "production":
    from pathlib import Path
    from dotenv import load_dotenv

    if os.getenv("PYTHON_ENV") is None:
        os.environ["PYTHON_ENV"] = "development"
    base_dir = Path(__file__).parents[1]
    load_dotenv(base_dir.joinpath(".env.local").resolve())

BASE_URL = os.getenv("BASE_URL")
API_PATH = os.getenv("API_PATH")

SERVER_URI = "".join([BASE_URL, API_PATH])
