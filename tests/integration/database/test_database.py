"""Integration tests for database class."""

import pytest

from app.database import Database

from asyncpg.exceptions import UndefinedTableError


class TestDatabase:
    async def test_database(self):
        db: Database = Database()

        await db.sql.engine.execute(
            "create table databaseconnectiontest (id int primary key)"
        )

        await db.sql.engine.execute(
            "insert into databaseconnectiontest (id) values (1), (2)"
        )

        check_query = await db.sql.engine.fetch("select id from databaseconnectiontest")

        assert check_query

        await db.sql.engine.execute("drop table databaseconnectiontest")

        with pytest.raises(UndefinedTableError):
            await db.sql.engine.fetch("select id from databaseconnectiontest")
