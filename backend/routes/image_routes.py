# image_routes.py
from flask import Blueprint, request, send_file, render_template, jsonify, after_this_request
from services.image_service import process_image
from services.automatic_upload import download_images_in_memory
from services.zip_service import create_zip_from_output
from werkzeug.utils import secure_filename
import os
import pandas as pd

image_blueprint = Blueprint('image', __name__)

# Configuration
OUTPUT_FOLDER = 'output'
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

processing_status = 'idle'

# Helper function to read the name list
def read_name_list(name_list_file_path):
    if name_list_file_path.endswith('.csv'):
        df = pd.read_csv(name_list_file_path, header=0, dtype=(str))
    elif name_list_file_path.endswith(('.xlsx', '.xls')):
        df = pd.read_excel(name_list_file_path, header=0, dtype=(str))
    else:
        raise ValueError('Unsupported file type for name list.')

    # Assuming names are in columns: name, surname, position, trikotnummer
    names_list = df.values.tolist()
    return names_list

@image_blueprint.route('/upload/manual', methods=['GET', 'POST'])
def upload_manual():
    if request.method == 'POST':
        # Check required files
        if 'background' not in request.files or 'image' not in request.files:
            return {"error": "Background and image must be provided"}, 400

        # Get form data
        name = request.form.get('name', '')
        surname = request.form.get('surname', '')
        position = request.form.get('position', '')
        trikotnummer = request.form.get('trikotnummer', '')
        image_file = request.files['image']
        background_file = request.files['background']

        # Read files into memory
        image_file_content = image_file.read()
        background_file_content = background_file.read()

        # Process image
        result = process_image(
            image_file_content,
            background_file_content,
            name,
            surname,
            position,
            trikotnummer
        )

        if 'error' in result:
            return result, 400

        # Return processed PDF
        pdf_path = result.get('pdf_path')
        return send_file(pdf_path, mimetype='application/pdf', as_attachment=True,
                         download_name=os.path.basename(pdf_path))
    else:
        # Render manual upload form
        return render_template('manual_upload.html')

@image_blueprint.route('/upload/automatic', methods=['GET', 'POST'])
def upload_automatic():
    global processing_status  # Global variable to track processing status
    
    if request.method == 'POST':
        try:
            processing_status = "in progress"  # Set status to in progress
            
            # Check required files
            if 'background' not in request.files or 'name-list' not in request.files:
                processing_status = "idle"
                return {"error": "Background and name list must be provided"}, 400

            folder_id = request.form.get('folder-id')
            if not folder_id:
                processing_status = "idle"
                return {"error": "Folder ID must be provided"}, 400

            background_file = request.files['background']
            name_list_file = request.files['name-list']

            # Read background file into memory
            background_file_content = background_file.read()

            # Save name list file temporarily
            name_list_filename = secure_filename(name_list_file.filename)
            name_list_file_path = os.path.join(UPLOAD_FOLDER, name_list_filename)
            name_list_file.save(name_list_file_path)

            # Download images from Google Drive
            images = download_images_in_memory(folder_id)
            # Read names from the uploaded name list
            names_list = read_name_list(name_list_file_path)

            # Check if counts match
            if len(images) != len(names_list):
                processing_status = "idle"
                return {"error": "Number of images and names do not match"}, 400

            # Process each image
            for image_data, name_data in zip(images, names_list):
                # Unpack name data
                name, surname, position, trikotnummer = name_data

                # Extract the actual content (which should be in bytes) from the dictionary
                result = process_image(
                    image_file_content=image_data['content'],  # Access the 'content' key
                    background_file_content=background_file_content,
                    name=name,
                    surname=surname,
                    position=position,
                    trikotnummer=trikotnummer
                )

                if 'error' in result:
                    processing_status = "idle"
                    return result, 400

            # Processing completed, set status to completed
            processing_status = "completed"
            return {"message": "Automatic processing completed successfully"}, 200

        except Exception as e:
            processing_status = "idle"
            return {"error": str(e)}, 500
    else:
        # Render automatic upload form
        return render_template('automatic_upload.html')


@image_blueprint.route('/check_processing_status', methods=['GET'])
def check_processing_status():
    global processing_status
    return jsonify({"status": processing_status})


@image_blueprint.route('/download_zip', methods=['GET'])
def download_zip():
    global processing_status
    if processing_status == "completed":
        zip_filename = create_zip_from_output(OUTPUT_FOLDER)

        @after_this_request
        def clear_output_directory(response):
            try:
                # Clear all files in the output directory
                for filename in os.listdir(OUTPUT_FOLDER):
                    file_path = os.path.join(OUTPUT_FOLDER, filename)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                print(f"Cleared all files in")
            except Exception as e:
                print(f"Error clearing output directory: {e}")
            return response
    
        return send_file(zip_filename)
    else:
        return {"error": "Processing not completed yet"}, 400
