CREATE SCHEMA IF NOT EXISTS aircrafts;

CREATE TABLE IF NOT EXISTS aircrafts.aircraft(
    id SERIAL PRIMARY KEY,
    manufacturer_serial_number TEXT NOT NULL UNIQUE,
    type TEXT NOT NULL,
    model TEXT NOT NULL,
    operator_airline TEXT,
    number_of_engines INTEGER NOT NULL
);
