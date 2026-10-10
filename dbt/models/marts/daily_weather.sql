SELECT
    DATE(forecast_time) AS forecast_date,

    AVG(temperature_c)
        AS avg_temperature_c,

    MIN(temperature_c)
        AS min_temperature_c,

    MAX(temperature_c)
        AS max_temperature_c,

    AVG(relative_humidity_pct)
        AS avg_humidity_pct,

    SUM(precipitation_mm)
        AS total_precipitation_mm

FROM {{ ref('stg_weather') }}

GROUP BY
    DATE(forecast_time)