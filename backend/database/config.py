import logging

import databases
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from core.config import settings

DATABASE_URL = settings.SQLALCHEMY_DATABASE_URI

engine = create_async_engine(DATABASE_URL, future=True, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()


async def check_db_connection():
    try:
        if "sqlite" not in DATABASE_URL:
            if settings.NODE_ENV == "production":
                database = databases.Database(DATABASE_URL)
            else:
                database = databases.Database(DATABASE_URL, force_rollback=True)
            if not database.is_connected:
                await database.connect()
                await database.execute("SELECT 1")
        logging.info("Database is connected")
    except Exception as e:
        logging.error("Looks like there is a problem in connection, see below traceback")
        raise e


async def wait_for_shutdown():
    async with databases.Database(DATABASE_URL) as database:
        if database.is_connected:
            await database.disconnect()
