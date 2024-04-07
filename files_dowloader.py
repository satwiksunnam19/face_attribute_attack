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

# Define the function to download files from a folder
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

# Search for the first shared folder by name
folder_name1 = 'images1024x1024'
query1 = f"name='{folder_name1}' and sharedWithMe and mimeType='application/vnd.google-apps.folder' and trashed=false"
results1 = drive_downloader.files().list(q=query1, pageSize=1000).execute()
items1 = results1.get('files', [])

# Search for the second shared folder by name
folder_name2 = 'stylegan2-config-f-psi-1.0'
query2 = f"name='{folder_name2}' and sharedWithMe and mimeType='application/vnd.google-apps.folder' and trashed=false"
results2 = drive_downloader.files().list(q=query2, pageSize=1000).execute()
items2 = results2.get('files', [])

# Check if both folders exist
if not items1:
    print(f"Shared folder '{folder_name1}' not found.")
if not items2:
    print(f"Shared folder '{folder_name2}' not found.")

# Get the ID of the first shared folder and download its files
if items1:
    folder_id1 = items1[0]['id']
    output_directory1 = './output1'
    if not os.path.exists(output_directory1):
        os.makedirs(output_directory1)
    download_files_from_folder(folder_id1, output_directory1)
    print(f"Download completed for folder '{folder_name1}'.")

# Get the ID of the second shared folder and download its files
if items2:
    folder_id2 = items2[0]['id']
    output_directory2 = './output2'
    if not os.path.exists(output_directory2):
        os.makedirs(output_directory2)
    download_files_from_folder(folder_id2, output_directory2)
    print(f"Download completed for folder '{folder_name2}'.")
