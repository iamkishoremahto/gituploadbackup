import os
import io
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

# Set up the Google Drive API client


credentials = service_account.Credentials.from_service_account_info(credentials_info, scopes=['https://www.googleapis.com/auth/drive'])
drive_service = build("drive", "v3", credentials=credentials)

# Get the repository data
repo_path = os.getcwd()
repo_name = os.path.basename(repo_path)

# Create a new folder in Google Drive
folder_metadata = {
    "name": repo_name,
    "mimeType": "application/vnd.google-apps.folder",
    # "parents": [os.environ.get("GOOGLE_DRIVE_FOLDER_ID")]
    "parents": ["1kD9MbDD8tMx_WdDpCjfkG2gl_rrMEr51"]
}
folder = drive_service.files().create(body=folder_metadata, fields="id").execute()
folder_id = folder.get("id")

# Upload repository files to the folder
for root, dirs, files in os.walk(repo_path):
    for file in files:
        file_path = os.path.join(root, file)
        
        file_metadata = {
            "name": file,
            "parents": [folder_id]
        }
        media = MediaIoBaseUpload(io.FileIO(file_path, "r"), mimetype="application/octet-stream")
        drive_service.files().create(body=file_metadata, media_body=media).execute()
