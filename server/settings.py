import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(BASE_DIR)

if os.getenv("NODE_ENV", "development") != "production":
    from dotenv import load_dotenv
    load_dotenv(BASE_DIR.joinpath(".env"))

DATABASE_URL = os.getenv("DATABASE_URL")
HASH_SCHEME = os.getenv("HASH_SCHEME")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_DAYS = os.getenv("ACCESS_TOKEN_EXPIRE_DAYS")