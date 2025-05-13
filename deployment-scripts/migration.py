"""Run pending database migrations."""

import asyncio
import logging
import os
import sys

from datetime import datetime
from pathlib import Path
from subprocess import call  # nosec
from typing import Iterator

from asyncpg.exceptions import UndefinedTableError
from pydantic import BaseModel, ConfigDict, DirectoryPath, FilePath
from pypika import Query, Schema

script_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(script_dir, "../.."))
from app.database import Database  # noqa: E402


logging.basicConfig(
    format="%(asctime)s %(levelname)s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)


class Migration(BaseModel):
    """Migration class.

    Attributes:
        date: When was the migration run.
        name: Migration name.
    """

    date: datetime = datetime.now()
    name: str


class Migrate(BaseModel):
    """Class for running the migrations."""

    db_schema: Schema
    database: Database = Database()
    model_config = ConfigDict(arbitrary_types_allowed=True)

    async def __call__(self, path: DirectoryPath) -> None:
        """Run pending migrations."""
        if not await self._check_schema_exists():
            await self._create_schema()

        if not await self._check_if_migrations_table_exists():
            await self._create_migration_table()

        ran_migrations: list[Migration] = await self._get_ran_migrations()

        for p in self._get_migrations_from_files(Path(path)):
            if p.stem in [m.name for m in ran_migrations]:
                logging.info(f"Migration {p.stem} was already run. Skipping.")
                continue
            logging.info(f"Running {p}")
            if p.suffix == ".sql":
                with p.open("r") as file:
                    await self.database.sql.engine.execute(file.read())
            else:
                rc = call(p)  # nosec
                if rc != 0:  # nosec
                    logging.error("Migration failed.")
                    exit(1)
            await self._add_migration_to_db(migration=Migration(name=p.stem))
        logging.info("All pending migrations run successfully.")

    async def _check_if_migrations_table_exists(self) -> bool:
        """Check if the migrations table exists.

        Returns:
            Whether the migrations table already exists or not.
        """
        query: Query = Query.from_(self.migrations_table).select("name")
        try:
            await self.database.sql.engine.fetch(str(query))
            return True

        except UndefinedTableError:
            return False

    async def _check_schema_exists(self) -> bool:
        """Check if the schema exists.

        Returns:
            Whether the schema already exists or not.
        """
        [(result,)] = await self.database.sql.engine.fetch(
            "SELECT EXISTS(SELECT 1 FROM information_schema.schemata "
            f"WHERE schema_name = '{self.db_schema._name}');"
        )

        return result

    async def _create_migration_table(self) -> None:
        """Create migrations table."""
        logging.info("Creating migration table pymigrations.")
        await self.database.sql.engine.execute(
            f"create table if not exists {self.migrations_table} "
            "(date TIMESTAMPTZ default now(), name VARCHAR(255) not null)"
        )

    async def _create_schema(self) -> None:
        """Create schema."""
        schema_name: str = self.db_schema._name
        logging.info(f"Creating schema {schema_name}.")
        query: str = f"create schema if not exists {schema_name}"
        await self.database.sql.engine.execute(query)

    async def _get_ran_migrations(self) -> list[Migration]:
        """Create migrations table."""
        query: Query = (
            Query.from_(self.migrations_table)
            .select(self.migrations_table.date)
            .select(self.migrations_table.name)
        )
        query_result: list[tuple] = await self.database.sql.engine.fetch(str(query))

        return [Migration(date=row[0], name=row[1]) for row in query_result]

    async def _add_migration_to_db(self, migration: Migration) -> None:
        """Add a migrations to the migrations table.

        Arguments:
            migration: The migration to add to the migrations table.
        """
        query: Query = Query.into(self.migrations_table).insert(
            migration.date, migration.name
        )
        await self.database.sql.engine.execute(str(query))

    def _get_migrations_from_files(self, path: Path) -> Iterator[FilePath]:
        """Discover migrations in the migrations directory."""
        for p in sorted(path.iterdir()):
            if not p.is_file():
                continue
            yield p

    @property
    def migrations_table(self) -> str:
        """Migrations table."""
        return self.db_schema.pymigrations


def main():
    """Main function."""
    if len(sys.argv) != 3:
        print("Usage: python migration.py path <arg2>")
        sys.exit(1)

    path = sys.argv[1]
    db_schema = sys.argv[2]

    migrate = Migrate(db_schema=Schema(db_schema))
    asyncio.run(migrate(path=path))


if __name__ == "__main__":
    main()
