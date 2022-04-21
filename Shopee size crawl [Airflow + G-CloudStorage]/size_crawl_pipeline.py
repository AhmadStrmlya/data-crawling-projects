import airflow
from datetime import timedelta, datetime

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.contrib.operators.bigquery_operator import BigQueryOperator
from airflow.contrib.operators.gcs_to_bq import GoogleCloudStorageToBigQueryOperator
from airflow.operators.python_operator import PythonOperator

from size_crawler import crawl_size

date_string = '2021-12-01'
start_date = datetime.strptime(date_string, '%Y-%m-%d')

default_args = {
    'owner': 'swakala',
    'depends_on_past': False,
    'start_date': airflow.utils.dates.days_ago(0),
    'email': [],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=2),
}

dag = DAG(
    'crawl_size_data_dev',
    schedule_interval='0 0 * * *',
    default_args=default_args
)

BQ_CONN_ID = "bigquery_default"
BQ_PROJECT = "manifest-setup-333302"
BQ_DATASET = "jawadwipa"

t1 = BashOperator(
    task_id='task_start',
    bash_command='echo "task start"',
    dag = dag
)

t2 = PythonOperator(
    task_id= 'python_crawler_csv_to_gcs',
    python_callable=crawl_size,
    dag = dag
)
t3 = GoogleCloudStorageToBigQueryOperator(
    task_id='csv_from_gcs_to_bq',
    bucket= 'asia-southeast1-airflow-env-932e6e6a-bucket',
    source_objects = ['dags/data/scrape_result.csv'],
    schema_fields=[
        {'name': 'crawl_ts', 'type': 'TIMESTAMP', 'mode': 'NULLABLE'},
        {'name': 'brand_id', 'type': 'STRING', 'mode': 'NULLABLE'},
        {'name': 'product_id', 'type': 'STRING', 'mode': 'NULLABLE'},
        {'name': 'size', 'type': 'STRING', 'mode': 'NULLABLE'},
        {'name': 'stock', 'type': 'INTEGER', 'mode': 'NULLABLE'},
    ],
    destination_project_dataset_table='manifest-setup-333302:jawadwipa.size_stock_dev_2',
    write_disposition='WRITE_APPEND',
    google_cloud_storage_conn_id=BQ_CONN_ID,
    bigquery_conn_id=BQ_CONN_ID,
    dag = dag
)

t4 = BashOperator(
    task_id='task_end',
    bash_command='echo "task ended"',
    dag = dag
)

t1 >> t2 >> t3 >> t4