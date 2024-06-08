from flask import Flask, request, send_file
from flask_cors import CORS
from rembg import remove
from PIL import Image, ImageDraw, ImageFont
import io
import os

app = Flask(__name__)
CORS(app)

# Constants for font sizes (pt)
NAME_FONT_SIZE = 40
SURNAME_FONT_SIZE = 50
POSITION_FONT_SIZE = 40
TRIKOTNUMMER_FONT_SIZE = 80

# Constants for text positions (start points)
NAME_X, NAME_Y = 75, 75
POSITION_X, POSITION_Y = 570, 850
TRIKOTNUMMER_X, TRIKOTNUMMER_Y = 90, 810

# Desired dimensions for the background in pixels
BG_WIDTH = 815
BG_HEIGHT = 1063

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

def draw_rotated_text(image, name, surname, name_font, surname_font, x, y, angle, fill=(255, 255, 255, 255)):
    if not name or not surname:
        print("Either name or surname is empty.")
        return
    
    # Define the space between name and surname
    space_width = name_font.getbbox(' ')[2] - name_font.getbbox(' ')[0]

    # Create a temporary image to calculate the size of the text
    temp_image = Image.new('RGBA', (1, 1), (255, 255, 255, 0))
    temp_draw = ImageDraw.Draw(temp_image)
    name_bbox = temp_draw.textbbox((0, 0), name, font=name_font)
    surname_bbox = temp_draw.textbbox((0, 0), surname, font=surname_font)
    
    name_width, name_height = name_bbox[2] - name_bbox[0], name_bbox[3] - name_bbox[1]
    surname_width, surname_height = surname_bbox[2] - surname_bbox[0], surname_bbox[3] - surname_bbox[1]

    print(f"Name bbox: {name_bbox}, Surname bbox: {surname_bbox}")
    print(f"Name width/height: {name_width}/{name_height}, Surname width/height: {surname_width}/{surname_height}")

    # Add extra padding to the text image to ensure descenders are not cut off
    padding = 25
    padded_width = name_width + space_width + surname_width + padding * 2
    padded_height = max(name_height, surname_height) + padding * 2

    # Create a new image with enough space to rotate the text
    text_image = Image.new('RGBA', (padded_width, padded_height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(text_image)

    # Adjust the y position to align text to the bottom
    bottom_y = padding + padded_height - max(name_height, surname_height)

    # Draw the name
    draw.text((padding, bottom_y - name_height), name, font=name_font, fill=fill)
    # Draw the surname next to the name with a space in between
    draw.text((padding + name_width + space_width, bottom_y - surname_height), surname, font=surname_font, fill=fill)

    # Rotate the text image
    rotated_text_image = text_image.rotate(angle, expand=True)

    # Calculate new position to place the rotated text
    new_x = x 
    new_y = y 

    # Paste the rotated text image onto the original image
    image.paste(rotated_text_image, (new_x, new_y), rotated_text_image)

    # Debug output
    print(f"Draw rotated text at ({new_x}, {new_y}) with size {rotated_text_image.size}")

# Example usage
@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files or 'background' not in request.files:
        return {"error": "Both image and background must be provided"}, 400

    image_file = request.files['image']
    background_file = request.files['background']
    name = request.form.get('name', '')
    surname = request.form.get('surname', '')
    position = request.form.get('position', '')
    trikotnummer = request.form.get('trikotnummer', '')

     # Debug: Print retrieved form values
    print(f"Received name: '{name}', surname: '{surname}', position: '{position}', trikotnummer: '{trikotnummer}'")
    print(f"Form keys: {request.form.keys()}")

    img = Image.open(image_file.stream).convert("RGBA")
    background = Image.open(background_file.stream).convert("RGBA")

    # Resize the background to the desired dimensions
    background = background.resize((BG_WIDTH, BG_HEIGHT), Image.LANCZOS)

    output_img = remove(img)
    output_img = output_img.resize(background.size, Image.LANCZOS)
    combined = Image.alpha_composite(background, output_img)

    # Update the font paths
    font_path_regular = os.path.join(ASSETS_DIR, "Roboto-Regular.ttf")
    font_path_bold = os.path.join(ASSETS_DIR, "Roboto-Bold.ttf")

    name_font = load_font(font_path_regular, NAME_FONT_SIZE)
    surname_font = load_font(font_path_regular, SURNAME_FONT_SIZE)
    position_font = load_font(font_path_regular, POSITION_FONT_SIZE)
    trikotnummer_font = load_font(font_path_bold, TRIKOTNUMMER_FONT_SIZE)

    # Draw rotated text with background color
    draw_rotated_text(combined, name, surname, name_font, surname_font, NAME_X, NAME_Y, -90, fill=(255, 255, 255, 255))
    draw = ImageDraw.Draw(combined)
    draw_text(draw, position, position_font, POSITION_X, POSITION_Y)
    draw_text(draw, trikotnummer, trikotnummer_font, TRIKOTNUMMER_X, TRIKOTNUMMER_Y)

    output = io.BytesIO()
    combined.save(output, format='PNG')
    output.seek(0)

    return send_file(output, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
