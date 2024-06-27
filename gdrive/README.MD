gcs - s3 : needs billing, access via service account with role storage admin
bucket: test-fzhang-0723

Yes, you can create a test Google Cloud Storage (GCS) bucket. Here are the steps to create a GCS bucket for testing purposes:

### Step 1: Create a Google Cloud Project

1. **Go to the Google Cloud Console**:
   - Navigate to [Google Cloud Console](https://console.cloud.google.com/).

2. **Create a New Project**:
   - If you don’t have an existing project, create a new one by clicking on the project drop-down at the top of the page and selecting "New Project".
   - Provide a name for your project and click "Create".

### Step 2: Enable the Google Cloud Storage API

1. **Enable the API**:
   - In the Google Cloud Console, navigate to the "API & Services" dashboard.
   - Click on "Enable APIs and Services".
   - Search for "Cloud Storage" and click on "Google Cloud Storage JSON API".
   - Click "Enable".

### Step 3: Create a GCS Bucket

1. **Navigate to Cloud Storage**:
   - In the Google Cloud Console, navigate to the "Storage" section from the left-hand menu.

2. **Create a Bucket**:
   - Click on "Create bucket".
   - Provide a globally unique name for your bucket (e.g., `my-test-bucket-unique-id`).
   - Select the location type and location (e.g., "Region" and "us-central1").
   - Choose the default storage class (e.g., "Standard").
   - Set access control settings (e.g., "Uniform" for simplified permissions).
   - Click "Create".

### Step 4: Create a Service Account and Download Credentials

1. **Create Service Account**:
   - In the Google Cloud Console, navigate to "IAM & Admin" > "Service Accounts".
   - Click "Create Service Account".
   - Provide a name and description for the service account, then click "Create".
   - Assign a role to the service account, such as "Storage Admin", and click "Continue".
   - Click "Done".

2. **Generate Key for the Service Account**:
   - Find your newly created service account in the list and click on it.
   - Go to the "Keys" tab and click "Add Key" > "Create New Key".
   - Select "JSON" and click "Create". This will download the JSON key file to your computer.

### Step 5: Use the GCS Bucket in Your Application

Ensure the downloaded JSON key file is accessible to your application. You can now use this key file to authenticate and interact with your GCS bucket.

### Example: Using the Test GCS Bucket in Your Application

Here is an example of how to use the created GCS bucket in your `main.py` application:

#### `gcs.py` - Updated for GCS Operations

```python
from google.cloud import storage

def upload_to_gcs(bucket_name, destination_blob_name, file_buffer, credentials_json):
    client = storage.Client.from_service_account_json(credentials_json)
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_file(file_buffer)
    print(f"File {destination_blob_name} uploaded to {bucket_name}.")
```

#### `main.py` - Main Application Using the Test GCS Bucket

```python
import json
import os
from flask import Flask, session, redirect, url_for
from auth import get_credentials, authorize, oauth2callback
from google_utils import get_file_metadata, list_files_in_folder, download_file
from gcs import upload_to_gcs

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Ensure this is set to a secure random value in production

FOLDER_ID = 'your_google_drive_folder_id'
GCS_BUCKET_NAME = 'your_test_gcs_bucket_name'
METADATA_STORAGE_PATH = 'path_to_store_metadata'
GCS_CREDENTIALS_JSON = 'path_to_your_gcs_credentials.json'  # Path to your downloaded JSON key file

@app.route('/')
def index():
    return redirect(url_for('authorize_route'))

@app.route('/authorize')
def authorize_route():
    return authorize()

@app.route('/oauth2callback')
def oauth2callback_route():
    return oauth2callback()

@app.route('/upload')
def upload():
    credentials = get_credentials()
    if not credentials:
        return redirect(url_for('authorize_route'))

    # List files in the specified folder
    files = list_files_in_folder(credentials, FOLDER_ID)
    print("Files in folder:")
    for file in files:
        print(f"ID: {file['id']}, Name: {file['name']}")
        
        # Get and save metadata for each file
        file_metadata = get_file_metadata(credentials, file['id'])
        metadata_filename = os.path.join(METADATA_STORAGE_PATH, f"{file['id']}_metadata.json")
        with open(metadata_filename, 'w') as metadata_file:
            json.dump(file_metadata, metadata_file)
        print(f"Metadata stored in {metadata_filename}.")

        # Download file from Google Drive
        file_buffer = download_file(credentials, file['id'])
        
        # Upload file to GCS
        upload_to_gcs(GCS_BUCKET_NAME, file['name'], file_buffer, GCS_CREDENTIALS_JSON)

    return "Files and metadata processed successfully!"

if __name__ == '__main__':
    app.run('localhost', 8080, debug=True)
```

### Running the Application

1. Ensure you have the necessary credentials and permissions set up.
2. Replace the placeholders with your actual values (`path_to_your_gcs_credentials.json`, `your_google_drive_folder_id`, etc.).
3. Create the directory specified in `METADATA_STORAGE_PATH` if it doesn't exist.
4. Run the application:
   ```bash
   python main.py
   ```

This application will now interact with your test GCS bucket, listing files in a specified Google Drive folder, retrieving their metadata, and storing both the metadata and files in GCS.

gdrive : access via oauth, use auto-generated client id as client_secrets 
