from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
import io
import os

# Define the scopes
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

# Obtain your Google credentials
def get_credentials():
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
    return creds

# Build the downloader
creds = get_credentials()
drive_downloader = build('drive', 'v3', credentials=creds)

# Function to download files
def download_files_from_folder(folder_id, output_directory):
    query = f"'{folder_id}' in parents and trashed=false"
    results = drive_downloader.files().list(q=query, pageSize=1000).execute()
    items = results.get('files', [])

    for item in items:
        if 'image' in item['mimeType']:
            request = drive_downloader.files().get_media(fileId=item['id'])
            file_path = os.path.join(output_directory, item['name'])
            with io.FileIO(file_path, 'wb') as f:
                downloader = MediaIoBaseDownload(f, request)
                done = False
                while done is False:
                    status, done = downloader.next_chunk()
                    print(f"Download {int(status.progress() * 100)}%: {item['name']}")
        else:
            print(f"Skipping non-image file: {item['name']}")

        if item['mimeType'] == 'application/vnd.google-apps.folder':
            subfolder_id = item['id']
            subfolder_path = os.path.join(output_directory, item['name'])
            if not os.path.exists(subfolder_path):
                os.makedirs(subfolder_path)
            download_files_from_folder(subfolder_id, subfolder_path)

# Search for the shared folder by name
folder_name = 'images1024x1024'
query = f"name='{folder_name}' and sharedWithMe and mimeType='application/vnd.google-apps.folder' and trashed=false"
results = drive_downloader.files().list(q=query, pageSize=1000).execute()
items = results.get('files', [])

if not items:
    print("Shared folder not found.")
else:
    # Get the ID of the shared folder
    folder_id = items[0]['id']
    output_directory = './output'
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    download_files_from_folder(folder_id, output_directory)
    print("Download completed.")
