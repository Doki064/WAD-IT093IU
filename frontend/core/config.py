import os

if os.getenv("NODE_ENV", "development") != "production":
    from pathlib import Path
    from dotenv import load_dotenv

    base_dir = Path(__file__).parents[1]
    load_dotenv(base_dir.joinpath(".env").resolve())

SERVER_URI = os.getenv("SERVER_URI")
