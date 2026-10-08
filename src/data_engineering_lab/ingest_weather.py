import logging

import pandas as pd
import requests
from sqlalchemy.dialects.postgresql import insert

from data_engineering_lab.database import get_engine

API_URL = "https://api.open-meteo.com/v1/forecast"

PARAMS = {
    "latitude": 48.8566,
    "longitude": 2.3522,
    "hourly": "temperature_2m,relative_humidity_2m,precipitation",
    "forecast_days": 2,
    "timezone": "UTC",
}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger(__name__)


def extract() -> dict:
    response = requests.get(
        API_URL,
        params=PARAMS,
        timeout=30,
    )

    response.raise_for_status()

    return response.json()


def transform(data: dict) -> pd.DataFrame:
    hourly = data["hourly"]

    dataframe = pd.DataFrame(
        {
            "forecast_time": pd.to_datetime(
                hourly["time"],
                utc=True,
            ),
            "temperature_2m": hourly["temperature_2m"],
            "relative_humidity_2m": hourly["relative_humidity_2m"],
            "precipitation": hourly["precipitation"],
        }
    )

    dataframe["latitude"] = data["latitude"]
    dataframe["longitude"] = data["longitude"]
    dataframe["ingested_at"] = pd.Timestamp.now(tz="UTC")

    return dataframe


def load(dataframe: pd.DataFrame) -> None:
    engine = get_engine()

    records = dataframe.to_dict(orient="records")

    statement = insert_weather_records(records)

    with engine.begin() as connection:
        connection.execute(statement)


def insert_weather_records(records: list[dict]):
    from sqlalchemy import MetaData, Table

    engine = get_engine()

    metadata = MetaData()

    weather_table = Table(
        "weather_hourly",
        metadata,
        schema="raw",
        autoload_with=engine,
    )

    statement = insert(weather_table).values(records)

    return statement.on_conflict_do_update(
        index_elements=[
            "forecast_time",
            "latitude",
            "longitude",
        ],
        set_={
            "temperature_2m": statement.excluded.temperature_2m,
            "relative_humidity_2m": statement.excluded.relative_humidity_2m,
            "precipitation": statement.excluded.precipitation,
            "ingested_at": statement.excluded.ingested_at,
        },
    )


def main() -> None:
    logger.info("Démarrage du pipeline météo")

    logger.info("Extraction des données depuis Open-Meteo")
    data = extract()

    logger.info("Transformation des données")
    dataframe = transform(data)

    logger.info("%s lignes obtenues", len(dataframe))

    logger.info("Chargement dans PostgreSQL")
    load(dataframe)

    logger.info("Pipeline terminé avec succès")


if __name__ == "__main__":
    main()
