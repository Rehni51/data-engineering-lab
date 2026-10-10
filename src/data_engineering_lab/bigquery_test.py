from google.cloud import bigquery


def main() -> None:
    client = bigquery.Client()

    query = """
    SELECT
        CURRENT_TIMESTAMP() AS current_time,
        'Hello BigQuery' AS message
    """

    result = client.query(query).result()

    for row in result:
        print(row.current_time, row.message)


if __name__ == "__main__":
    main()
