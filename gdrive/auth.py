import json
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Configuration from environment variables
CLIENT_SECRETS_FILE = os.getenv(
    "GDRIVE_CLIENT_SECRETS_FILE",
    "/Users/frankzhang/Projects/vid-ingest/client_secrets.json",
)
TOKEN_FILE = os.getenv(
    "GDRIVE_TOKEN_FILE", "/Users/frankzhang/Projects/vid-ingest/token.json"
)
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]
PORT = int(os.getenv("GDRIVE_AUTH_SERVER_PORT", 8888))


def get_credentials():
    credentials = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as token:
            credentials = Credentials.from_authorized_user_info(
                json.load(token), SCOPES
            )

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE, SCOPES
            )
            credentials = flow.run_local_server(port=PORT)

        with open(TOKEN_FILE, "w") as token:
            token.write(credentials.to_json())

    return credentials
