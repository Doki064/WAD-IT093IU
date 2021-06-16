import os
import secrets
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseSettings, AnyHttpUrl, PostgresDsn, validator

if os.getenv("NODE_ENV", "development") != "production":
    from pathlib import Path
    from dotenv import load_dotenv

    base_dir = Path(__file__).parents[1]
    load_dotenv(base_dir.joinpath(".env.local").resolve())


class PostgresAsyncpgDsn(PostgresDsn):
    allowed_schemes = {
        "postgres",
        "postgresql",
        "postgres+asyncpg",
        "postgresql+asyncpg",
    }


class Settings(BaseSettings):
    PROJECT_NAME: str = "Wholesale Management System"

    NODE_ENV: str = "development"
    SERVER_SOFTWARE: str

    API_PATH: str = "/api/v1"

    SCHEMES: List[str]
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    SERVER_DOMAIN: str
    SERVER_URL: AnyHttpUrl
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[PostgresAsyncpgDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresAsyncpgDsn.build(
            scheme="postgresql+asyncpg",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_HOST"),
            path=f"/{values.get('POSTGRES_DB', '')}",
        )

    FIRST_SUPERUSER: str
    FIRST_SUPERUSER_PASSWORD: str


settings = Settings()
