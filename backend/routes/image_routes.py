from flask import Blueprint, request, send_file
from services.image_service import process_image
from services.folder_loop import folder_automation

image_blueprint = Blueprint('image', __name__)

@image_blueprint.route('/upload', methods=['POST'])
def upload_image():
    if 'background' not in request.files:
        return {"error": "background must be provided"}, 400
    
    folder_id = request.form.get('folder-id')
    image_file = request.files['image']
    background_file = request.files['background']
    name = request.form.get('name', '')
    surname = request.form.get('surname', '')
    position = request.form.get('position', '')
    trikotnummer = request.form.get('trikotnummer', '')
    
    result = None

    if 'folder-id' in request.form and folder_id:
        images_used = folder_automation(folder_id)
        print("Automatic processing of folder contents")

        for image in images_used:
            result = process_image(image, background_file, name, surname, position, trikotnummer)
            if 'error' in result:
                return result, 400

    elif image_file:
        result = process_image(image_file, background_file, name, surname, position, trikotnummer)
        print("Manually uploaded image used")

    if result and 'error' in result:
        return result, 400
    
    if result:
        return send_file(result['output'], mimetype='image/png')
    else:
        return {"error": "No valid image processing path was found."}, 400
