from airflow.decorators import task


@task
def save_to_db(processed_data):
    print(f"Saving to DB: {processed_data}")
    return processed_data
