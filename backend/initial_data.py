import asyncio
import logging

from database import init_db
from database.config import async_session

logger = logging.getLogger(__name__)


async def init():
    db = async_session()
    await init_db(db)


async def main():
    logger.info("Creating initial data")
    await init()
    logger.info("Initial data created")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
