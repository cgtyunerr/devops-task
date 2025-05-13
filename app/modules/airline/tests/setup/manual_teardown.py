"""Manual teardown for airline module."""

import asyncio
import logging
import os

from manual_setup import check, database

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)


async def teardown():
    logging.info("Checking test teardown conditions...")
    await check()
    logging.info("Removing dummy data.")
    with open(
        os.path.join(os.path.dirname(__file__), "dummy_data_destroy.sql"), "r"
    ) as file:
        await database.sql.engine.execute(file.read())


if __name__ == "__main__":
    asyncio.run(teardown())
    logging.info("Done.")
