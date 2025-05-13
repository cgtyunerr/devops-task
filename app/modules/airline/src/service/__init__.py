"""Airline service module."""

from pypika import Schema, Table

airline_schema: Schema = Schema("airlines")

airline_table: Table = airline_schema.airline
