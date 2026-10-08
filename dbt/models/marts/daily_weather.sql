SELECT
    forecast_time::DATE AS forecast_date,

    ROUND(
        AVG(temperature_c),
        2
    ) AS avg_temperature_c,

    MIN(temperature_c)
        AS min_temperature_c,

    MAX(temperature_c)
        AS max_temperature_c,

    ROUND(
        AVG(relative_humidity_pct),
        1
    ) AS avg_humidity_pct,

    SUM(precipitation_mm)
        AS total_precipitation_mm

FROM {{ ref('stg_weather') }}

GROUP BY
    forecast_time::DATE