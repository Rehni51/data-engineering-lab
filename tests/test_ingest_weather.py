import pandas as pd

from data_engineering_lab.ingest_weather import transform


def test_transform_returns_expected_rows():
    raw_data = {
        "latitude": 48.8566,
        "longitude": 2.3522,
        "hourly": {
            "time": [
                "2026-10-07T10:00",
                "2026-10-07T11:00",
            ],
            "temperature_2m": [
                15.2,
                16.1,
            ],
            "relative_humidity_2m": [
                70,
                68,
            ],
            "precipitation": [
                0.0,
                0.2,
            ],
        },
    }

    dataframe = transform(raw_data)

    assert len(dataframe) == 2

    assert list(dataframe.columns) == [
        "forecast_time",
        "temperature_2m",
        "relative_humidity_2m",
        "precipitation",
        "latitude",
        "longitude",
        "ingested_at",
    ]

    assert dataframe.iloc[0]["temperature_2m"] == 15.2
    assert dataframe.iloc[0]["latitude"] == 48.8566

    assert pd.api.types.is_datetime64_any_dtype(dataframe["forecast_time"])


def test_transform_adds_coordinates_to_every_row():
    raw_data = {
        "latitude": 48.8566,
        "longitude": 2.3522,
        "hourly": {
            "time": [
                "2026-10-07T10:00",
                "2026-10-07T11:00",
            ],
            "temperature_2m": [15.2, 16.1],
            "relative_humidity_2m": [70, 68],
            "precipitation": [0.0, 0.2],
        },
    }

    dataframe = transform(raw_data)

    assert (dataframe["latitude"] == 48.8566).all()
    assert (dataframe["longitude"] == 2.3522).all()
