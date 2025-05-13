CREATE SCHEMA IF NOT EXISTS airlines;

CREATE TABLE IF NOT EXISTS airlines.airline(
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    callsign TEXT NOT NULL UNIQUE,
    founded_year TEXT NOT NULL,
    base_airport TEXT NOT NULL
);
