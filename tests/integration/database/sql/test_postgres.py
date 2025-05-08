"""Integration test for psql."""

import pytest

from app.database.sql import SqlEngine
from asyncpg import UndefinedTableError


@pytest.fixture
def psql() -> SqlEngine:
    return SqlEngine(
        host="localhost",
        name="postgres",
        password="dbpass",
        user="dbuser",
        port=5432,
    )


class TestPsqlConnection:
    async def test_psql(self, psql):
        await psql.execute("create table psqlconnectiontest (id int primary key)")

        await psql.execute("insert into psqlconnectiontest (id) values (1), (2)")

        check_query = await psql.fetch("select id from psqlconnectiontest")

        assert check_query

        await psql.execute("drop table psqlconnectiontest")

        with pytest.raises(UndefinedTableError):
            await psql.fetch("select id from psqlconnectiontest")


class TestPsqlContextManager:
    async def test_context_manager(self, psql):
        async with psql() as conn:
            try:
                await conn.execute(
                    "create table psqlcontextmanager (id int primary key)"
                )
                await conn.execute(
                    "insert into psqlcontextmanager (id) values (1), (2)"
                )

                [[check_val]] = await conn.fetch(
                    "select id from psqlcontextmanager where id =1"
                )
                assert check_val == 1
            finally:
                await conn.execute("drop table psqlcontextmanager")

    async def test_context_manager_error(self, psql):
        try:
            async with psql() as conn:
                await conn.execute(
                    "create table psqlcontextmanager (id int primary key)"
                )
                await conn.execute(
                    "insert into psqlcontextmanager (id) values " "(1), (2)"
                )

                await conn.fetch("select id from psqlcontextmanager1 where id =1")
        except UndefinedTableError:
            pass

        with pytest.raises(UndefinedTableError):
            await psql.fetch("select id from psqlcontextmanager")
