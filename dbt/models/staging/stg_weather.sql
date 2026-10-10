SELECT
    forecast_time,

    latitude,
    longitude,

    temperature_2m AS temperature_c,

    relative_humidity_2m
        AS relative_humidity_pct,

    precipitation
        AS precipitation_mm,

    ingested_at

FROM {{ source('raw', 'weather_hourly') }}

WHERE forecast_time IS NOT NULL