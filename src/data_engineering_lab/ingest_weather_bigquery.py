import logging
import os

from google.api_core.exceptions import NotFound
from google.cloud import bigquery

from data_engineering_lab.bigquery import get_bigquery_client
from data_engineering_lab.ingest_weather import extract, transform

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger(__name__)


def load_bigquery(dataframe) -> None:
    client = get_bigquery_client()

    project_id = os.environ["GCP_PROJECT_ID"]

    dataset_id = f"{project_id}.raw"

    try:
        dataset = client.get_dataset(dataset_id)
    except NotFound:
        dataset = bigquery.Dataset(dataset_id)
        dataset.location = client.location
        dataset = client.create_dataset(dataset, exists_ok=True)
        logger.info("Dataset %s disponible dans %s", dataset_id, dataset.location)

    table_id = f"{dataset_id}.weather_hourly"

    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    )

    load_job = client.load_table_from_dataframe(
        dataframe,
        table_id,
        job_config=job_config,
        location=dataset.location,
    )

    load_job.result()

    table = client.get_table(table_id)

    logger.info(
        "%s lignes présentes dans %s",
        table.num_rows,
        table_id,
    )


def main() -> None:
    logger.info("Démarrage ingestion météo BigQuery")

    logger.info("Extraction Open-Meteo")
    data = extract()

    logger.info("Transformation")
    dataframe = transform(data)

    logger.info("%s lignes obtenues", len(dataframe))

    logger.info("Chargement BigQuery")
    load_bigquery(dataframe)

    logger.info("Pipeline BigQuery terminé")


if __name__ == "__main__":
    main()
