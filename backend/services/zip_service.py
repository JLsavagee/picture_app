# services/zip_service.py
import zipfile
import os
from flask import send_file

def create_zip_from_output(output_dir, zip_filename="processed_pdfs.zip"):
    # Create a ZIP file from the PDFs in the output directory
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for root, dirs, files in os.walk(output_dir):
            for file in files:
                if file.endswith('.pdf'):
                    zipf.write(os.path.join(root, file), file)
    return zip_filename
