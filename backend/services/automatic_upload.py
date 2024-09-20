from google.oauth2 import service_account
from googleapiclient.discovery import build
import io
from googleapiclient.http import MediaIoBaseDownload
from PIL import Image
import pandas as pd
from services.image_service import process_image

# Authenticate and initialize the Google Drive API
SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'team-cards-photo-edit-9a387c2ffb58.json'  # Replace with your service account file

credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

service = build('drive', 'v3', credentials=credentials)

def download_images_in_memory(folder_id):
    # List to store images and their filenames
    images = []

    # Fetch files in the folder
    results = service.files().list(
        q=f"'{folder_id}' in parents and mimeType contains 'image/'",
        spaces='drive',
        fields='files(id, name)'
    ).execute()

    items = results.get('files', [])

    # Sort the items list by the name property to ensure the images are downloaded in name order
    items.sort(key=lambda x: x['name'])

    for item in items:
        file_id = item['id']
        file_name = item['name']

        # Download the file into memory
        request = service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)

        done = False
        while not done:
            status, done = downloader.next_chunk()

        # Reset file handle position
        fh.seek(0)

        # Read the content
        image_content = fh.read()

            # Ensure image_content is bytes
        if not isinstance(image_content, bytes):
            print(f"Error: image_content for {file_name} is not bytes, it is {type(image_content)}")
            continue  # Skip this image if it's not in bytes format

        # Append the image content and name
        images.append({'filename': file_name, 'content': image_content})

    return images

def read_name_list(name_list_file_path):
    if name_list_file_path.endswith('.csv'):
        df = pd.read_csv(name_list_file_path, header=0, dtype=str) 
    elif name_list_file_path.endswith(('.xlsx', '.xls')):
        df = pd.read_excel(name_list_file_path, header=0, dtype=str)  
    else:
        raise ValueError('Unsupported file type for name list.')

    # Assuming names are in columns: name, surname, position, trikotnummer
    names_list = df.values.tolist()
    return names_list

def automatic_process(folder_id, name_list_file_path, background_file_path):
    # Download images into memory
    images = download_images_in_memory(folder_id)

    # Read names
    names_list = read_name_list(name_list_file_path)

    # Read background file content into memory
    with open(background_file_path, 'rb') as bg_file:
        background_file_content = bg_file.read()

    # Check if counts match
    if len(images) != len(names_list):
        raise ValueError('Number of images and names do not match.')

    # Process each image
    for image_data, name_data in zip(images, names_list):
        # Unpack name data
        name, surname, position, trikotnummer = name_data

         # Check if the content is bytes
        if not isinstance(image_data['content'], bytes):
            print(f"Error: image_data['content'] for {image_data['filename']} is not bytes, it is {type(image_data['content'])}")
            continue  # Skip processing this image if it's not bytes


        # Call the processing function
        result = process_image(
            image_file_content=image_data['content'],
            background_file_content=background_file_content,
            name=name,
            surname=surname,
            position=position,
            trikotnummer=trikotnummer
        )

        # Handle result as needed
        print(f"Processed image for {name} {surname}")

if __name__ == '__main__':
    # Example usage
    folder_id = 'your_google_drive_folder_id'
    name_list_file_path = 'path/to/your/name_list.csv'  # Or .xlsx
    background_file_path = 'path/to/your/background_image.png'

    automatic_process(folder_id, name_list_file_path, background_file_path)