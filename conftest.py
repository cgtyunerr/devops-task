"""Test configuration."""

import os

import pytest

from fastapi.testclient import TestClient
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend

from app.api.app import app
from tests import database


@pytest.fixture(scope="module", autouse=True)
def set_env_variable():
    os.environ["AIOCACHE_DISABLE"] = "1"


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as client:
        yield client


@pytest.fixture(autouse=True, scope="function")
async def run_after_test():
    """Code run after each test function."""
    FastAPICache.init(
        InMemoryBackend(),
        prefix="fastapi-cache",
    )
    yield
    await FastAPICache.clear()
    # Code to run after each test function
    pool = await database.sql.engine._get_pool()
    await pool.close()
