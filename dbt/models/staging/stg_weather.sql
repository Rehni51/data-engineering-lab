SELECT
    forecast_time,

    latitude,
    longitude,

    temperature_2m::NUMERIC(6, 2) AS temperature_c,

    relative_humidity_2m::INTEGER
        AS relative_humidity_pct,

    precipitation::NUMERIC(8, 2)
        AS precipitation_mm,

    ingested_at

FROM {{ source('raw', 'weather_hourly') }}

WHERE forecast_time IS NOT NULL