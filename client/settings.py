import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(BASE_DIR)

if os.getenv("NODE_ENV", "development") != "production":
    from dotenv import load_dotenv
    load_dotenv(BASE_DIR.joinpath(".env"))

SERVER_HOST = os.getenv("SERVER_HOST")
SERVER_PORT = os.getenv("SERVER_PORT")
