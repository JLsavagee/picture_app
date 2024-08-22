from google.oauth2 import service_account
from googleapiclient.discovery import build
import io
from googleapiclient.http import MediaIoBaseDownload
from PIL import Image


# Authenticate and initialize the Google Drive API
SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'team-cards-photo-edit-0f642ef15086.json'  # Replace with your service account file

credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

service = build('drive', 'v3', credentials=credentials)


folder_id = '10TZJod3vKArx0XBPf6XLIcultMxtj-87'  # Extract this from the provided link

# List to store the images
images = []

# Query to find all files in the specified folder
results = service.files().list(
    q=f"'{folder_id}' in parents and mimeType contains 'image/'",
    spaces='drive',
    fields='files(id, name)').execute()

items = results.get('files', [])

for item in items:
    file_id = item['id']
    file_name = item['name']
    
    # Download the file from Google Drive
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
    
    # Reset file handle position
    fh.seek(0)
    
    # Store the image content in the list
    images.append(fh.getvalue())

# Now `images` contains the binary content of all downloaded images


