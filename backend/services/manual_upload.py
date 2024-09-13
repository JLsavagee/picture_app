# manual.py

import os
from flask import Flask, request, render_template, send_file
from werkzeug.utils import secure_filename
from image_service import process_image

app = Flask(__name__)

@app.route('/manual', methods=['GET', 'POST'])
def manual_upload():
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        surname = request.form.get('surname')
        position = request.form.get('position')
        trikotnummer = request.form.get('trikotnummer')

        # Get uploaded files
        image_file = request.files.get('image')
        background_file = request.files.get('background')

        if not all([name, surname, position, trikotnummer, image_file, background_file]):
            return 'All fields are required.', 400

        # Read file content into memory
        image_file_content = image_file.read()
        background_file_content = background_file.read()

        # Call the processing function
        result = process_image(
            image_file_content,
            background_file_content,
            name,
            surname,
            position,
            trikotnummer
        )

        # Return the processed PDF file to the user
        return send_file(
            result['pdf_path'],
            mimetype='application/pdf',
            as_attachment=True,
            download_name=os.path.basename(result['pdf_path'])
        )
    else:
        # Render the manual upload form
        return render_template('manual_upload.html')

if __name__ == '__main__':
    app.run(debug=True)
