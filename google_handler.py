import os

from dotenv import load_dotenv

from gdrive.auth import get_credentials
from gdrive.drive import (
    download_file,
    get_folder_id_from_url,
    is_video_file,
    list_files_in_folder,
    list_files_in_folder_no_auth,
)
from gdrive.gcs import upload_to_gcs

# Load environment variables from .env file
load_dotenv()

# Configuration
GCS_BUCKET_NAME = os.getenv("GCS_BUCKET_NAME")
GCS_CREDENTIALS_JSON = os.getenv("GCS_CREDENTIALS_JSON")


def main(folder_url):
    try:
        folder_id = get_folder_id_from_url(folder_url)
    except ValueError as e:
        print(e)
        return

    # Try to list files without authentication
    try:
        files = list_files_in_folder_no_auth(folder_id)
        print("Accessed the folder without OAuth.")
    except Exception:
        print("The folder is private or requires OAuth.")
        # Authenticate and get credentials
        credentials = get_credentials()
        # List files in the specified folder with authentication
        files = list_files_in_folder(credentials, folder_id)

    print("Files in folder:")
    for file in files:
        if is_video_file(file):
            print(f"ID: {file['id']}, Name: {file['name']}")
            # Download and upload each file to GCS
            file_buffer = download_file(credentials, file["id"])
            upload_to_gcs(
                GCS_BUCKET_NAME, file["name"], file_buffer, GCS_CREDENTIALS_JSON
            )


if __name__ == "__main__":

    main("https://drive.google.com/drive/folders/12ttmcHo1ZShjaYt3AMoJ4J-zWnxrDcxz")

    # import sys

    # if len(sys.argv) != 2:
    #     print("Usage: python main.py <google_drive_folder_url>")
    #     sys.exit(1)
    # folder_url = sys.argv[1]
    # main(folder_url)
