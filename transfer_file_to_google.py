import os
import io
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

# Set up the Google Drive API client
credentials_info = {
  "type": "service_account",
  "project_id": "helenzystools",
  "private_key_id": "b4a7bbcff1dc735dde337bb367a9276a49654212",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCHOAtTRqb0XSxr\nSZGQXcDt+l8mIzqLr6u6BdoUK4bE9tQx9U+YkgrBDtZ2M83SpS3o+heiMZz729zz\n7r+kRTPmeMMEksSAyNahy1UgtP3VuHH982uzfrNSKsGEeu886xYsS3AsuD7UOe85\n9losvjbAKTD0mKgltFp/7SB7GGHMd0MqBEfGJ5ldy6EET4SbpkPb2LEhN2DwejSA\nW7iCMnPSBlBWVr6frFnnSrLc7RSD8F5ChwQNXuSnsAjBP+483O1bmMw3CpLusAaC\n3uKoEDilOut39L3LPFv0wdXYE8fUVUL5stGjESg2llu2dLAXUOJ+h49h0KYDYB0U\nHeij90f1AgMBAAECggEAGFim8V+PQABmtwqQAwZebnreFufQ6sW+jcfv9CHCKkSn\nADfDFR12gjxBsRaywHKtSX1+M93q/g4gQmuCZflv1td3haNHbki7HHaX5UOxUIHd\nRHRHuBHgB7NbFJdt6/IIFAGhOOwTo/KqeC07H0NAaGkCP4gc/mzyvoXbi05gjYfI\nuCq/yFfbfeZ1dHAH13rKpAqxjQuBQ4UlY8jwxutNw0CSto5oJi3k93RHTh5Z0Qra\nuTCnhPfBnG6yExfubw41kQylglhHd+TbafGtztaEBnr7Oaaap3IpIx6N4fbS57IK\nz8yUkwyONWASvQPTp0iHGhQriVLHwM6kL4lcCLK3IQKBgQC6hVs4s7LZKLKeTUgX\ne9o7G+HC8kqcPV5tJZ4FGynVkJN41Af1rkE1b2Grp0hS0w7IR7YQBG5/VbeqXHDH\nW5D3iC9e7kLNLM6cp9unzjjHvt3xO7HuK/7BRJ/o8yHOIAFsvqv88NeyQuYPjuOT\nm1WT6Il/OXrRAhoNkzT6vWekJwKBgQC5lobeaIyeaXhlO9s/1fonqzH+KAvfRn6w\nE8qeZ6Otu9gSMOJWpDohZt/bPz19fst2TeC7VSW1lliNkCfOu+F31nzllTHHJF5N\n8D/7JLmzQ8J5AbtXY0IaqQX16HzkCqcXRn6qWxK60CVykwf8IoIGJ7YWdcd9dAf9\n1wxudqR4gwKBgF0V3r++ltxfvjzYrsjhi7kCIjqLdwbgbbalFmbP9qHZxG+ByfMn\nou2LB8CF/McxA+iaOVdnDspHuiCwf6xOm1udwJ5s5DPHT9nIwAvQFHBDZjpVI2iM\n1lgX6oJ0jIN1X6Coy+axP8R8NJrBIfxxglUNsUkoI44ZsWzi8YbNbeLzAoGAQu66\n7XOfY3J+bWRNCpTNh4kCmrsurPPrtO0uYjrWmU3p+4WN29mW7X0Atz3zm1MjZiNo\nLafj1b3HaibXdIPmKSY+HT7VmRDQwiMnsBfqsXB6rtGlEztFGABlme6jPEtrP8W4\n4Q+/jYiMOOo2MwTvB/FCho8rx18VksMARMadQqkCgYEArlUbqBRScvjss2a+PYVk\nN0MZcbZwjtZ0UIgV0bfmpHcbgW0ek55aBx9cRDrbdv4oRGkgr7R+E+Pwm2b8bXrx\ntVdZnd43gEbLzTiB0IkdEVy0s/9GKotyAVAys84vZg8kH/SbAh3MKo+R88uLrnVW\ne0GQEYOqolDcEK+1q7kOds8=\n-----END PRIVATE KEY-----\n",
  "client_email": "helenzystools@helenzystools.iam.gserviceaccount.com",
  "client_id": "109050453058032428437",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/helenzystools%40helenzystools.iam.gserviceaccount.com"
}

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
        media = MediaIoBaseUpload(io.FileIO(file_path, "rb"), mimetype="application/octet-stream")
        drive_service.files().create(body=file_metadata, media_body=media).execute()
