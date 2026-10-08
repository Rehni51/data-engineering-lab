SELECT
    forecast_time,
    temperature_2m,
    relative_humidity_2m,
    precipitation,
    ingested_at
FROM raw.weather_hourly
ORDER BY forecast_time
LIMIT 10;