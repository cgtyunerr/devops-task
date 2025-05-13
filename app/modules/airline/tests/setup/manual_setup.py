"""Manual setup for airline module."""

import asyncio
import logging
import os
from sys import exit

from tests import database

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)


async def check():
    if os.getenv("DB__HOST") not in ("localhost", "127.0.0.1"):
        logging.error("`DB__HOST` must be localhost for testing.")
        exit(1)


async def setup():
    logging.info("Checking test setup conditions...")
    await check()
    logging.info("Creating dummy data.")
    with open(
        os.path.join(os.path.dirname(__file__), "dummy_data_create.sql"), "r"
    ) as file:
        await database.sql.engine.execute(file.read())


if __name__ == "__main__":
    asyncio.run(setup())
    logging.info("Done.")
