from flask import Blueprint, request, send_file
from backend.services.image_service import process_image

image_blueprint = Blueprint('image', __name__)

@image_blueprint.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files or 'background' not in request.files:
        return {"error": "Both image and background must be provided"}, 400

    image_file = request.files['image']
    background_file = request.files['background']
    name = request.form.get('name', '')
    surname = request.form.get('surname', '')
    position = request.form.get('position', '')
    trikotnummer = request.form.get('trikotnummer', '')
    zoom_factor = request.form.get('dimension', '')

    result = process_image(image_file, background_file, name, surname, position, trikotnummer, zoom_factor)

    if 'error' in result:
        return result, 400

    return send_file(result['output'], mimetype='image/png')
