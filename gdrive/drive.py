import io
import re

from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload


def get_folder_id_from_url(url):
    match = re.search(r"folders/([a-zA-Z0-9_-]+)", url)
    if match:
        return match.group(1)
    else:
        raise ValueError("Invalid Google Drive folder URL")


def get_file_metadata(credentials, file_id):
    service = build("drive", "v3", credentials=credentials)
    file_metadata = service.files().get(fileId=file_id).execute()
    return file_metadata


def list_files_in_folder(credentials, folder_id):
    service = build("drive", "v3", credentials=credentials)
    query = f"'{folder_id}' in parents and trashed=false"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    items = results.get("files", [])
    return items


def download_file(credentials, file_id):
    service = build("drive", "v3", credentials=credentials)
    request = service.files().get_media(fileId=file_id)
    file_buffer = io.BytesIO()
    downloader = MediaIoBaseDownload(file_buffer, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
        print(f"Download {int(status.progress() * 100)}% complete.")
    file_buffer.seek(0)
    return file_buffer
