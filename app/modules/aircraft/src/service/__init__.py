"""Aircraft service module."""

from pypika import Schema, Table

aircraft_schema: Schema = Schema("aircrafts")

aircraft_table: Table = aircraft_schema.aircraft
