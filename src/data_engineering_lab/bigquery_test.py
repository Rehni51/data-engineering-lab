from google.cloud import bigquery

client = bigquery.Client()

query = """
SELECT
    CURRENT_TIMESTAMP() AS current_time,
    'Hello BigQuery' AS message
"""

result = client.query(query).result()

for row in result:
    print(row.current_time, row.message)
