from flask import Flask, request, send_file
from flask_cors import CORS
from rembg import remove
from PIL import Image, ImageDraw, ImageFont
import io
import os

app = Flask(__name__)
CORS(app)

# Constants for font sizes
NAME_FONT_SIZE = 60
POSITION_FONT_SIZE = 40
TRIKOTNUMMER_FONT_SIZE = 80

# Constants for text positions (start points)
NAME_X, NAME_Y = 75, 75
POSITION_X, POSITION_Y = 570, 850
TRIKOTNUMMER_X, TRIKOTNUMMER_Y = 90, 810

# Path to assets directory
ASSETS_DIR = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'assets', 'fonts')

def load_font(font_path, font_size):
    try:
        print(f"Attempting to load font from {font_path} with size {font_size}")
        font = ImageFont.truetype(font_path, font_size)
        print(f"Successfully loaded font: {font_path}")
        return font
    except IOError as e:
        print(f"Error loading font from {font_path}. Error: {e}")
        return ImageFont.load_default()

def draw_text(draw, text, font, x, y, fill=(255, 255, 255, 255)):
    draw.text((x, y), text, font=font, fill=fill)

def draw_rotated_text(image, text, font, x, y, angle, fill=(255, 255, 255, 255)):
    # Create a temporary image to calculate the size of the text
    temp_image = Image.new('RGBA', (1, 1), (255, 255, 255, 0))
    temp_draw = ImageDraw.Draw(temp_image)
    bbox = temp_draw.textbbox((0, 0), text, font=font)
    width, height = bbox[2] - bbox[0], bbox[3] - bbox[1]

    # Add extra padding to the text image to ensure descenders are not cut off
    padding = 25
    padded_width = width + padding * 2
    padded_height = height + padding * 2

    # Create a new image with enough space to rotate the text
    text_image = Image.new('RGBA', (padded_width, padded_height))
    draw = ImageDraw.Draw(text_image)
    draw.text((padding, padding), text, font=font, fill=fill)

    # Rotate the text image
    rotated_text_image = text_image.rotate(angle, expand=True)

    # Calculate new position to place the rotated text
    # Start position (most left point)
    new_x = x
    new_y = y

    # Paste the rotated text image onto the original image
    image.paste(rotated_text_image, (new_x, new_y), rotated_text_image)

# Example usage
@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files or 'background' not in request.files:
        return {"error": "Both image and background must be provided"}, 400

    image_file = request.files['image']
    background_file = request.files['background']
    name = request.form['name']
    position = request.form['position']
    trikotnummer = request.form['trikotnummer']

    img = Image.open(image_file.stream).convert("RGBA")
    background = Image.open(background_file.stream).convert("RGBA")

    output_img = remove(img)
    output_img = output_img.resize(background.size, Image.LANCZOS)
    combined = Image.alpha_composite(background, output_img)

    # Update the font paths
    font_path_regular = os.path.join(ASSETS_DIR, "Roboto-Regular.ttf")
    font_path_bold = os.path.join(ASSETS_DIR, "Roboto-Bold.ttf")

    name_font = load_font(font_path_regular, NAME_FONT_SIZE)
    position_font = load_font(font_path_regular, POSITION_FONT_SIZE)
    trikotnummer_font = load_font(font_path_bold, TRIKOTNUMMER_FONT_SIZE)

    # Draw rotated text with background color
    draw_rotated_text(combined, name, name_font, NAME_X, NAME_Y, -90, fill=(255, 255, 255, 255))
    draw = ImageDraw.Draw(combined)
    draw_text(draw, position, position_font, POSITION_X, POSITION_Y)
    draw_text(draw, trikotnummer, trikotnummer_font, TRIKOTNUMMER_X, TRIKOTNUMMER_Y)

    output = io.BytesIO()
    combined.save(output, format='PNG')
    output.seek(0)

    return send_file(output, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
