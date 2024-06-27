import json
import os

from gdrive.auth import get_credentials
from gdrive.drive import (
    download_file,
    get_file_metadata,
    get_folder_id_from_url,
    list_files_in_folder,
)
from gdrive.gcs import upload_to_gcs

# Configuration
GCS_BUCKET_NAME = "test-fzhang-0723"
METADATA_STORAGE_PATH = "test"
GCS_CREDENTIALS_JSON = "gcs_credential.json"  # Path to your downloaded JSON key file


def main():
    # Authenticate and get credentials
    credentials = get_credentials()

    # Prompt for Google Drive folder URL
    folder_url = input("Enter the Google Drive folder URL: ")
    try:
        folder_id = get_folder_id_from_url(folder_url)
    except ValueError as e:
        print(e)
        return

    # List files in the specified folder
    files = list_files_in_folder(credentials, folder_id)
    print("Files in folder:")
    for file in files:
        print(f"ID: {file['id']}, Name: {file['name']}")

        # Get and save metadata for each file
        file_metadata = get_file_metadata(credentials, file["id"])
        metadata_filename = os.path.join(
            METADATA_STORAGE_PATH, f"{file['id']}_metadata.json"
        )
        with open(metadata_filename, "w") as metadata_file:
            json.dump(file_metadata, metadata_file)
        print(f"Metadata stored in {metadata_filename}.")

        # Download and upload each file to GCS
        file_buffer = download_file(credentials, file["id"])
        upload_to_gcs(GCS_BUCKET_NAME, file["name"], file_buffer, GCS_CREDENTIALS_JSON)


if __name__ == "__main__":
    main()
