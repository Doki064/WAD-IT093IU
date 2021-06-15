import logging

import databases
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from settings import DATABASE_URL

engine = create_async_engine(DATABASE_URL, future=True, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()


async def check_db_connection():
    try:
        if "sqlite" not in str(DATABASE_URL):
            database = databases.Database(DATABASE_URL)
            if not database.is_connected:
                await database.connect()
                await database.execute("SELECT 1")
        logging.info("Database is connected")
    except Exception as e:
        logging.error("Looks like there is a problem in connection, see below traceback")
        raise e
