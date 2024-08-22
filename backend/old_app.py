from flask import Flask, request, send_file
from flask_cors import CORS
from rembg import remove
from PIL import Image, ImageDraw, ImageFont, ImageOps
from PyPDF2 import PdfWriter, PdfReader
import io
import os

app = Flask(__name__)
CORS(app)

# Constants for font sizes (pt)
NAME_FONT_SIZE = 55
SURNAME_FONT_SIZE = 80
POSITION_FONT_SIZE = 42
TRIKOTNUMMER_FONT_SIZE = 80

# Constants for text positions (start points)
NAME_X, NAME_Y = 80, 75
POSITION_X, POSITION_Y = 80, 858
TRIKOTNUMMER_X, TRIKOTNUMMER_Y = 0, 0


# Desired dimensions for the background in pixels
BG_WIDTH = 815
BG_HEIGHT = 1063

# Maximum width for the name+surname text box
MAX_TEXT_WIDTH = 700  

# Path to assets directory
ASSETS_DIR = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'assets', 'fonts')

#fixed layer imports
FIXED_PNG_PATH = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'assets', 'fixed_layers', 'Positionsfeld-Grün.png')
CAMP_LOGO_PNG_PATH = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'assets', 'fixed_layers', 'WLS_Logo.png')
SPONSOR_LOGO_PNG_PATH = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'assets', 'fixed_layers', 'DominosLogo.png')

backside = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'assets', 'fixed_layers', 'dominos_backside.png')

#transforming backside
backside_path = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'assets', 'fixed_layers', 'backside_pdf')
backside = Image.open(backside).convert("RGBA")
backside = backside.resize((BG_WIDTH, BG_HEIGHT), Image.LANCZOS)
backside.save(backside_path, format='PDF', resolution=300)

def merge_pdfs(pdf1_path, pdf2_path, output_pdf_path):
    reader1 = PdfReader(pdf1_path)
    reader2 = PdfReader(pdf2_path)
    writer = PdfWriter()

    # Add all pages from the first PDF
    for page in reader1.pages:
        writer.add_page(page)

    # Add all pages from the second PDF
    for page in reader2.pages:
        writer.add_page(page)

    # Save the combined PDF
    with open(output_pdf_path, 'wb') as f:
        writer.write(f)

def load_font(font_path, font_size):
    try:
        print(f"Attempting to load font from {font_path} with size {font_size}")
        font = ImageFont.truetype(font_path, font_size)
        print(f"Successfully loaded font: {font_path}")
        return font
    except IOError as e:
        print(f"Error loading font from {font_path}. Error: {e}")
        return ImageFont.load_default()

def get_text_width(draw, text, font):
    return draw.textbbox((0, 0), text, font=font)[2] - draw.textbbox((0, 0), text, font=font)[0]

def draw_text(draw, text, font, x, y, fill=(255, 255, 255, 255)):
    draw.text((x, y), text, font=font, fill=fill)

def draw_rotated_text(image, name, surname, name_font, surname_font, x, y, angle, fill=(255, 255, 255, 255)):
    if not name or not surname:
        print("Either name or surname is empty.")
        return
    
    # Create a temporary image to calculate the size of the text
    temp_image = Image.new('RGBA', (1, 1), (255, 255, 255, 0))
    temp_draw = ImageDraw.Draw(temp_image)
    name_bbox = temp_draw.textbbox((0, 0), name, font=name_font)
    surname_bbox = temp_draw.textbbox((0, 0), surname, font=surname_font)
    
    name_width, name_height = name_bbox[2] - name_bbox[0], name_bbox[3] - name_bbox[1]
    surname_width, surname_height = surname_bbox[2] - surname_bbox[0], surname_bbox[3] - surname_bbox[1]
    space_width = temp_draw.textbbox((0, 0), ' ', font=name_font)[2] - temp_draw.textbbox((0, 0), ' ', font=name_font)[0]

    print(f"Name bbox: {name_bbox}, Surname bbox: {surname_bbox}")
    print(f"Name width/height: {name_width}/{name_height}, Surname width/height: {surname_width}/{surname_height}")

    # Determine the total width and height needed for the combined text
    total_width = name_width + space_width + surname_width

        # Adjust font sizes if necessary
    while total_width > MAX_TEXT_WIDTH and name_font.size > 10 and surname_font.size > 10:
        name_font = ImageFont.truetype(name_font.path, name_font.size - 1)
        surname_font = ImageFont.truetype(surname_font.path, surname_font.size - 1)
        name_width = get_text_width(temp_draw, name, name_font)
        surname_width = get_text_width(temp_draw, surname, surname_font)
        total_width = name_width + space_width + surname_width

    max_height = max(name_height, surname_height)

    # Create a new image with enough space to rotate the text
    padded_width = total_width + 50
    padded_height = max_height + 50
    text_image = Image.new('RGBA', (padded_width, padded_height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(text_image)

    # Calculate y positions to align text to the bottom
    bottom_y = padded_height - 25

    # Draw the name aligned to the bottom
    name_y = bottom_y - name_height
    draw.text((25, name_y), name, font=name_font, fill=fill)
    
    # Draw the surname next to the name with a space in between, aligned to the bottom
    surname_y = bottom_y - surname_height
    draw.text((25 + name_width + space_width, surname_y), surname, font=surname_font, fill=fill)

    # Rotate the text image
    rotated_text_image = text_image.rotate(angle, expand=True)

    # Calculate new position to place the rotated text
    new_x = x 
    new_y = y 

    # Paste the rotated text image onto the original image
    image.paste(rotated_text_image, (new_x, new_y), rotated_text_image)

    # Debug output
    print(f"Draw rotated text at ({new_x}, {new_y}) with size {rotated_text_image.size}")


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
    zoom_factor = request.form.get('dimension', '')

    zoom_factor = float(zoom_factor)
    # Debug: Print retrieved form values
    print(f"Received name: '{name}', surname: '{surname}', position: '{position}', trikotnummer: '{trikotnummer}'")
    print(f"Form keys: {request.form.keys()}")

    img = Image.open(image_file.stream).convert("RGBA")
    background = Image.open(background_file.stream).convert("RGBA")

    # Resize the background to the desired dimensions
    background = background.resize((BG_WIDTH, BG_HEIGHT), Image.LANCZOS)

    output_img = remove(img)

    #Crop the output image to the desired dimensions while maintaining aspect ratio
    #Desired dimensions for cutted image
    IMG_WIDTH = int(output_img.width / zoom_factor)
    IMG_HEIGHT = int(output_img.height / zoom_factor)

    # Calculate position to paste output_img so it is centered on the background
    IMG_POSITION_X = (BG_WIDTH - IMG_WIDTH) // 2
    IMG_POSITION_Y = (BG_HEIGHT - IMG_HEIGHT) // 2

    IMG_POSITION_Y = IMG_POSITION_Y - 200
    IMG_POSITION_X = IMG_POSITION_X  + 0

    # Center crop the zoomed image to the desired dimensions
    output_img = ImageOps.fit(output_img, (IMG_WIDTH, IMG_HEIGHT), method=Image.LANCZOS, centering=(0.5, 0.5))

    # Create a new image with the same size as the background
    combined = background.copy()

    # Paste the output_img onto the combined image at the desired position
    combined.paste(output_img, (IMG_POSITION_X, IMG_POSITION_Y), output_img)

    # Update the font paths
    font_path_regular = os.path.join(ASSETS_DIR, "Impact.ttf")
    #font_path_bold = os.path.join(ASSETS_DIR, "Roboto-Bold.ttf")

    name_font = load_font(font_path_regular, NAME_FONT_SIZE)
    surname_font = load_font(font_path_regular, SURNAME_FONT_SIZE)
    position_font = load_font(font_path_regular, POSITION_FONT_SIZE)
    trikotnummer_font = load_font(font_path_regular, TRIKOTNUMMER_FONT_SIZE)

    # Load the position bubble overlay image
    overlay_img = Image.open(FIXED_PNG_PATH).convert("RGBA")
    overlay_img.thumbnail((BG_WIDTH, BG_HEIGHT), Image.LANCZOS)

    # Paste the overlay image onto the combined image
    combined.paste(overlay_img, (60, 830), overlay_img)

    # Load the camp logo overlay image
    camp_logo_img = Image.open(CAMP_LOGO_PNG_PATH).convert("RGBA")
    camp_logo_img.thumbnail((BG_WIDTH, BG_HEIGHT), Image.LANCZOS)

    # Paste the camp logo image onto the combined image
    combined.paste(camp_logo_img, (538, 942), camp_logo_img)

    # Load the camp logo overlay image
    sponsor_logo_img = Image.open(SPONSOR_LOGO_PNG_PATH).convert("RGBA")
    sponsor_logo_img.thumbnail((BG_WIDTH, BG_HEIGHT), Image.LANCZOS)

    # Paste the camp logo image onto the combined image
    combined.paste(sponsor_logo_img, (490, 75), sponsor_logo_img)

    # Draw rotated text with background color
    draw_rotated_text(combined, name, surname, name_font, surname_font, NAME_X, NAME_Y, -90, fill=(255, 255, 255, 255))
    draw = ImageDraw.Draw(combined)
    draw_text(draw, position, position_font, POSITION_X, POSITION_Y)
    draw_text(draw, trikotnummer, trikotnummer_font, TRIKOTNUMMER_X, TRIKOTNUMMER_Y)

    output = io.BytesIO()
    combined.save(output, format='PNG')
    output.seek(0)

    # Save the image as a PDF in the output directory
    output_dir = os.path.join(os.path.dirname(__file__), 'output')
    os.makedirs(output_dir, exist_ok=True)
    pdf_path = os.path.join(output_dir, f"{name}_{surname}.pdf")
    combined.save(pdf_path, format='PDF', resolution=300)

    # Merge the created PDFs
    merge_pdfs(pdf_path, backside_path, pdf_path)

    return send_file(output, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)