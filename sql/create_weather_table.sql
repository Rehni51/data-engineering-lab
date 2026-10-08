CREATE SCHEMA IF NOT EXISTS raw;

CREATE TABLE IF NOT EXISTS raw.weather_hourly (
    forecast_time TIMESTAMPTZ NOT NULL,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    temperature_2m DOUBLE PRECISION,
    relative_humidity_2m INTEGER,
    precipitation DOUBLE PRECISION,
    ingested_at TIMESTAMPTZ NOT NULL,

    PRIMARY KEY (
        forecast_time,
        latitude,
        longitude
    )
);