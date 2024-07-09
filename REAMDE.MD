# Google Drive to Google Cloud Storage Video File Transfer

This script transfers video files from a specified Google Drive folder to a Google Cloud Storage (GCS) bucket. It supports accessing public Google Drive folders without authentication and private folders with OAuth authentication.

## Prerequisites

1. **Python 3.x**
2. **Google Cloud SDK** for setting up the GCS bucket and service account credentials.
3. **Required Python packages**:
   - `google-auth`
   - `google-auth-oauthlib`
   - `google-auth-httplib2`
   - `google-api-python-client`
   - `google-cloud-storage`
   - `python-dotenv`

## Setup

### Google Cloud Setup

1. **Create a project in the [Google Cloud Console](https://console.cloud.google.com/)**.
2. **Enable the Google Drive API and Google Cloud Storage API**.
3. **Create a service account and download the JSON key file**. Save this file in your project directory as `gcs_credential.json`.
4. **Create a GCS bucket** to store the video files.
5. **Create a `.env` file** in your project directory with the following content:
   ```plaintext
   GCS_BUCKET_NAME=<your_gcs_bucket_name>
   GCS_CREDENTIALS_JSON=gcs_credential.json


### OAuth Client Setup
In the Google Cloud Console, create OAuth 2.0 credentials.
Download the client_secrets.json file and save it in your project directory.
Running the Script
Specify the Google Drive Folder URL:

Pass the Google Drive folder URL as a command-line argument when running the script.
Run the Script:

bash
Copy code
python main.py "https://drive.google.com/drive/folders/<your_google_drive_f
