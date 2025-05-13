"""Project test module."""

from app.database import Database

database: Database = Database()

user_10000_token: str = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpX"
    "VCJ9.eyJ1c2VyX2lkIjoxMDAwMH0.v0medZT2pcDtA0ZGAKtr46hdaf8P8M3t5Z4URMrSfUk"
)

user_40000_token: str = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo0MDAwMH0."
    "9wpsx27l9B9rdQLJlgmPX0x67h6b9xi7YBtPv33n8CE"
)


def mock_func_returning_id(*args, **kwargs):
    return 987


async def mock_async_func(*args, **kwargs):
    return None


async def mock_async_func_returning_id(*args, **kwargs):
    return 987


async def mock_async_func_returning_set_int(*args, **kwargs):
    return {987}


def mock_async_func_generator(return_value):
    async def mock_func(*args, **kwargs):
        return return_value

    return mock_func


def mock_func_generator(return_value):
    def mock_func(*args, **kwargs):
        return return_value

    return mock_func
