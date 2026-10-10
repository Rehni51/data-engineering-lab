from unittest.mock import Mock

import pandas as pd
import pytest
from google.api_core.exceptions import Forbidden, NotFound
from google.cloud import bigquery

from data_engineering_lab import ingest_weather_bigquery


@pytest.mark.parametrize("dataset_missing", [True, False])
def test_load_prepares_dataset_before_upload(monkeypatch, dataset_missing):
    project_id = "test-project"
    monkeypatch.setenv("GCP_PROJECT_ID", project_id)
    client = Mock(location="EU")
    monkeypatch.setattr(ingest_weather_bigquery, "get_bigquery_client", lambda: client)

    dataset = bigquery.Dataset(f"{project_id}.raw")
    dataset.location = "EU" if dataset_missing else "US"
    if dataset_missing:
        client.get_dataset.side_effect = NotFound("Dataset missing")
    else:
        client.get_dataset.return_value = dataset

    def create_dataset(requested_dataset, *, exists_ok):
        assert requested_dataset.reference == dataset.reference
        assert requested_dataset.location == "EU"
        assert exists_ok is True
        return dataset

    client.create_dataset.side_effect = create_dataset
    load_job = Mock()

    def upload(dataframe, table_id, *, job_config, location):
        if dataset_missing:
            client.create_dataset.assert_called_once()
        else:
            client.create_dataset.assert_not_called()
        assert table_id == f"{project_id}.raw.weather_hourly"
        assert location == dataset.location
        assert job_config.write_disposition == bigquery.WriteDisposition.WRITE_TRUNCATE
        return load_job

    client.load_table_from_dataframe.side_effect = upload
    client.get_table.return_value.num_rows = 1

    dataframe = pd.DataFrame({"temperature_2m": [15.2]})
    ingest_weather_bigquery.load_bigquery(dataframe)

    client.get_dataset.assert_called_once_with(f"{project_id}.raw")
    assert client.load_table_from_dataframe.call_args.args[0] is dataframe
    client.load_table_from_dataframe.assert_called_once()
    load_job.result.assert_called_once_with()
    client.get_table.assert_called_once_with(f"{project_id}.raw.weather_hourly")


def test_load_does_not_upload_when_dataset_creation_is_forbidden(monkeypatch):
    monkeypatch.setenv("GCP_PROJECT_ID", "test-project")
    client = Mock(location="EU")
    client.get_dataset.side_effect = NotFound("Dataset missing")
    client.create_dataset.side_effect = Forbidden("Dataset creation forbidden")
    monkeypatch.setattr(ingest_weather_bigquery, "get_bigquery_client", lambda: client)

    with pytest.raises(Forbidden):
        ingest_weather_bigquery.load_bigquery(pd.DataFrame())

    client.load_table_from_dataframe.assert_not_called()
