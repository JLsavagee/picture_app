from flask import Flask, request, send_file
from flask_cors import CORS
from rembg import remove
from PIL import Image, ImageDraw, ImageFont
import io

app = Flask(__name__)
CORS(app)

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files or 'background' not in request.files:
        return {"error": "Both image and background must be provided"}, 400
    
    image_file = request.files['image']
    background_file = request.files['background']
    name = request.form['name']
    position = request.form['position']
    trikotnummer = request.form['trikotnummer']
    
    # Open the images
    img = Image.open(image_file.stream).convert("RGBA")
    background = Image.open(background_file.stream).convert("RGBA")
    
    # Remove the background from the foreground image
    output_img = remove(img)
    
    # Resize the foreground image to fit the background
    output_img = output_img.resize(background.size, Image.LANCZOS)
    
    # Composite the foreground image onto the background
    combined = Image.alpha_composite(background, output_img)

    # Draw the text on the image
    draw = ImageDraw.Draw(combined)
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except IOError:
        font = ImageFont.load_default()

    # Rotate the name and draw it on the left side
    name_text = Image.new('RGBA', (combined.height, 40), (255, 255, 255, 0))
    draw_name = ImageDraw.Draw(name_text)
    draw_name.text((0, 0), name, font=font, fill=(255, 255, 255, 255))
    name_text = name_text.rotate(90, expand=1)
    combined.paste(name_text, (0, 0), name_text)

    # Draw the position and trikotnummer on the bottom right
    draw.text((combined.width - 150, combined.height - 60), f"{position}\n{trikotnummer}", font=font, fill=(255, 255, 255, 255))

    # Save the result to a BytesIO object
    output = io.BytesIO()
    combined.save(output, format='PNG')
    output.seek(0)

    return send_file(output, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
