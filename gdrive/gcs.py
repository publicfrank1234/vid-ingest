from google.cloud import storage


def upload_to_gcs(bucket_name, destination_blob_name, file_buffer, gcs_creds_json):
    client = storage.Client.from_service_account_json(gcs_creds_json)
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_file(file_buffer)
    print(f"File {destination_blob_name} uploaded to {bucket_name}.")
