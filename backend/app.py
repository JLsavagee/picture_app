from flask import Flask, request, send_file
from flask_cors import CORS
from rembg import remove
from PIL import Image
import io

app = Flask(__name__)
CORS(app)

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files or 'background' not in request.files:
        return {"error": "Both image and background must be provided"}, 400
    
    image_file = request.files['image']
    background_file = request.files['background']
    
    # Open the images
    img = Image.open(image_file.stream).convert("RGBA")
    background = Image.open(background_file.stream).convert("RGBA")
    
    # Remove the background from the foreground image
    output_img = remove(img)
    
    # Resize the foreground image to fit the background
    output_img = output_img.resize(background.size, Image.LANCZOS)
    
    # Composite the foreground image onto the background
    combined = Image.alpha_composite(background, output_img)
    
    # Save the result to a BytesIO object
    output = io.BytesIO()
    combined.save(output, format='PNG')
    output.seek(0)

    return send_file(output, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
