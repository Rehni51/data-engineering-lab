from datetime import timedelta
from pathlib import Path
import subprocess

import pendulum

from airflow.sdk import DAG, task


PROJECT_ROOT = Path("/home/hdrz/projects/data-engineering-lab")
UV_BIN = "/home/hdrz/.local/bin/uv"


with DAG(
    dag_id="weather_pipeline",
    description="Ingestion Open-Meteo puis transformations dbt",
    schedule="0 */6 * * *",
    start_date=pendulum.datetime(2026, 10, 1, tz="UTC"),
    catchup=False,
    default_args={
        "retries": 2,
        "retry_delay": timedelta(minutes=2),
    },
    tags=["learning", "weather"],
) as dag:

    @task
    def ingest_weather():
        subprocess.run(
            [
                UV_BIN,
                "run",
                "python",
                "-m",
                "data_engineering_lab.ingest_weather",
            ],
            cwd=PROJECT_ROOT,
            check=True,
        )

    @task
    def build_dbt():
        subprocess.run(
            [
                UV_BIN,
                "run",
                "--env-file",
                ".env",
                "dbt",
                "build",
                "--project-dir",
                "dbt",
            ],
            cwd=PROJECT_ROOT,
            check=True,
        )

    ingestion = ingest_weather()
    transformations = build_dbt()

    ingestion >> transformations
