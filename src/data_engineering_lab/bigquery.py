import os

from dotenv import load_dotenv
from google.cloud import bigquery

load_dotenv()


def get_bigquery_client() -> bigquery.Client:
    project_id = os.environ["GCP_PROJECT_ID"]
    location = os.getenv("BQ_LOCATION", "EU")

    return bigquery.Client(
        project=project_id,
        location=location,
    )
