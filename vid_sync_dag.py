from datetime import datetime, timedelta

from airflow.decorators import dag

from tasks.create_index import create_index
from tasks.fetch_user_urls import fetch_user_urls
from tasks.process_url import process_urls
from tasks.save_to_db import save_to_db

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2023, 1, 1),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


@dag(
    dag_id="sync_videos_dag",
    default_args=default_args,
    description="A dynamic DAG to sync videos from various sources",
    schedule_interval=timedelta(days=1),
    catchup=False,
)
def sync_videos_dag():
    user_id = "example_user_id"
    urls = fetch_user_urls(user_id)
    processed_data = process_urls(urls)
    indexed_data = create_index(processed_data)
    save_to_db(indexed_data)


sync_videos_dag()
