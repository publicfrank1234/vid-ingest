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


def is_video_file(file):
    """Determine if a file is a video based on its MIME type or file extension."""
    video_mime_types = [
        "video/mp4",
        "video/x-msvideo",
        "video/quicktime",
        "video/x-matroska",
        "video/webm",
        "video/x-flv",
        "video/mpeg",
    ]
    video_extensions = [
        ".mp4",
        ".avi",
        ".mov",
        ".mkv",
        ".webm",
        ".flv",
        ".mpeg",
        ".mpg",
    ]

    mime_type = file.get("mimeType")
    file_name = file.get("name", "").lower()

    # Check MIME type
    if mime_type in video_mime_types:
        return True

    # Check file extension
    for ext in video_extensions:
        if file_name.endswith(ext):
            return True

    return False


def check_permissions(credentials, file_id):
    """Check if a file or folder is publicly accessible."""
    service = build("drive", "v3", credentials=credentials)
    permissions = service.permissions().list(fileId=file_id).execute()
    for permission in permissions.get("permissions", []):
        if permission["type"] == "anyone" and permission["role"] == "reader":
            return True
    return False


def list_files_in_folder_no_auth(folder_id):
    """List and return files in the specified Google Drive folder without authentication."""
    service = build("drive", "v3")
    query = f"'{folder_id}' in parents and trashed=false"
    results = (
        service.files().list(q=query, fields="files(id, name, mimeType)").execute()
    )
    items = results.get("files", [])
    return items
