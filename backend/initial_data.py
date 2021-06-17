import asyncio
import logging

from database.init_db import init

logger = logging.getLogger(__name__)


async def main():
    logger.info("Creating initial data")
    await init()
    logger.info("Initial data created")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
