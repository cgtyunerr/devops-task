"""User service module."""

from pypika import Schema, Table

user_schema: Schema = Schema("users")

user_table: Table = user_schema.user
