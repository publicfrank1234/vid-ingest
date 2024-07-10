from airflow.decorators import task


@task
def create_index(processed_data):
    print(f"Creating Index")
    return processed_data
