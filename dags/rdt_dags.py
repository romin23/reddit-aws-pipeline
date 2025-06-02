from airflow import DAG
from datetime import datetime
import os, sys
from airflow.operators.python import PythonOperator

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from pipelines.reddit_pipeline import reddit_pipeline
from pipelines.s3_data_pipeline import uplaod_s3_pipeline


arguments_constants = {
    'owner': 'ROmin Katre',
    'start_date': datetime(year=2024, month=8, day=12)
}

postfix_file = datetime.now().strftime("%Y%m%d")

dag = DAG(
    dag_id = "reddit_etl_pipeline",
    default_args=arguments_constants,
    schedule_interval='@daily',
    catchup=False,
    tags = ['reddit', 'etl', 'pipeline']
)

# reddit data extraction
data_extract = PythonOperator(
    task_id = 'reddit_data_extraction',
    python_callable = reddit_pipeline,
    op_kwargs = {
        'file_name': f'reddit_data_{postfix_file}',
        'subreddit': 'dataengineering',
        'time_filter': 'day',
        'limit': 100 
    },
    dag = dag
)
# uploading data to s3
data_upload_s3 = PythonOperator(
    task_id = 'upload_data_to_s3',
    python_callable = uplaod_s3_pipeline,
    dag=dag
)

data_extract >> data_upload_s3