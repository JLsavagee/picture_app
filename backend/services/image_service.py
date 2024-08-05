import io
import os
from PIL import Image, ImageDraw, ImageFont, ImageOps
from rembg import remove
from utils.helpers import load_font, draw_rotated_text, draw_text, merge_pdfs

# Constants
NAME_FONT_SIZE = 55
SURNAME_FONT_SIZE = 80
POSITION_FONT_SIZE = 42
TRIKOTNUMMER_FONT_SIZE = 80

NAME_X, NAME_Y = 80, 75
POSITION_X, POSITION_Y = 80, 858
TRIKOTNUMMER_X, TRIKOTNUMMER_Y = 0, 0

BG_WIDTH = 815
BG_HEIGHT = 1063
MAX_TEXT_WIDTH = 700

BORDER_SIZE = 61
PADDING = 25

ASSETS_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'frontend', 'assets', 'fonts')

FIXED_PNG_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'frontend', 'assets', 'fixed_layers', 'Positionsfeld-Grün.png')
CAMP_LOGO_PNG_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'frontend', 'assets', 'fixed_layers', 'WLS_Logo.png')
SPONSOR_LOGO_PNG_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'frontend', 'assets', 'fixed_layers', 'DominosLogo.png')

backside = os.path.join(os.path.dirname(__file__), '..', '..', 'frontend', 'assets', 'fixed_layers', 'dominos_backside.png')

# Transforming backside
backside_path = os.path.join(os.path.dirname(__file__), '..', '..', 'frontend', 'assets', 'fixed_layers', 'backside_pdf')
backside_img = Image.open(backside).convert("RGBA")
backside_img = backside_img.resize((BG_WIDTH, BG_HEIGHT), Image.LANCZOS)
backside_img.save(backside_path, format='PDF', resolution=300)

def get_bounding_box(img):
    bbox = img.getbbox()
    return bbox

def process_image(image_file, background_file, name, surname, position, trikotnummer):
    img = Image.open(image_file.stream).convert("RGBA")
    background = Image.open(background_file.stream).convert("RGBA")

    background = background.resize((BG_WIDTH, BG_HEIGHT), Image.LANCZOS)

    output_img = remove(img)

    # Get the bounding box of the non-transparent pixels
    bbox = get_bounding_box(output_img)
    if bbox:
        non_transparent_region = output_img.crop(bbox)
    else:
        non_transparent_region = output_img

    # Calculate the maximum dimensions for the image to fit within the padding
    max_width = BG_WIDTH - 2 * PADDING
    max_height = BG_HEIGHT - BORDER_SIZE - PADDING  # Only top padding is applied

    # Calculate the scaling factor to fit the image within the maximum dimensions
    scale_factor = min(max_width / non_transparent_region.width, max_height / non_transparent_region.height)

    # Resize the image accordingly
    new_width = int(non_transparent_region.width * scale_factor)
    new_height = int(non_transparent_region.height * scale_factor)
    non_transparent_region = non_transparent_region.resize((new_width, new_height), Image.LANCZOS)

    # Calculate the position to ensure it has 50px distance from the left, right, and top edges, and sits on the bottom border
    IMG_POSITION_X = PADDING
    IMG_POSITION_Y = BG_HEIGHT - new_height - BORDER_SIZE

    combined = background.copy()
    combined.paste(non_transparent_region, (IMG_POSITION_X, IMG_POSITION_Y), non_transparent_region)
    # Draw a bounding box around the non-transparent region
    draw = ImageDraw.Draw(combined)
    bbox_outline = [IMG_POSITION_X, IMG_POSITION_Y, IMG_POSITION_X + new_width, IMG_POSITION_Y + new_height]
    draw.rectangle(bbox_outline, outline="red", width=5)

    font_path_regular = os.path.join(ASSETS_DIR, "Impact.ttf")
    
    name_font = load_font(font_path_regular, NAME_FONT_SIZE)
    surname_font = load_font(font_path_regular, SURNAME_FONT_SIZE)
    position_font = load_font(font_path_regular, POSITION_FONT_SIZE)
    trikotnummer_font = load_font(font_path_regular, TRIKOTNUMMER_FONT_SIZE)

    overlay_img = Image.open(FIXED_PNG_PATH).convert("RGBA")
    overlay_img.thumbnail((BG_WIDTH, BG_HEIGHT), Image.LANCZOS)
    combined.paste(overlay_img, (60, 830), overlay_img)

    camp_logo_img = Image.open(CAMP_LOGO_PNG_PATH).convert("RGBA")
    camp_logo_img.thumbnail((BG_WIDTH, BG_HEIGHT), Image.LANCZOS)
    combined.paste(camp_logo_img, (538, 942), camp_logo_img)

    sponsor_logo_img = Image.open(SPONSOR_LOGO_PNG_PATH).convert("RGBA")
    sponsor_logo_img.thumbnail((BG_WIDTH, BG_HEIGHT), Image.LANCZOS)
    combined.paste(sponsor_logo_img, (490, 75), sponsor_logo_img)

    draw_rotated_text(combined, name, surname, name_font, surname_font, NAME_X, NAME_Y, -90)
    draw = ImageDraw.Draw(combined)
    draw_text(draw, position, position_font, POSITION_X, POSITION_Y)
    draw_text(draw, trikotnummer, trikotnummer_font, TRIKOTNUMMER_X, TRIKOTNUMMER_Y)

    output = io.BytesIO()
    combined.save(output, format='PNG')
    output.seek(0)

    output_dir = os.path.join(os.path.dirname(__file__), '..', 'output')
    os.makedirs(output_dir, exist_ok=True)
    pdf_path = os.path.join(output_dir, f"{name}_{surname}.pdf")
    combined.save(pdf_path, format='PDF', resolution=300)

    merge_pdfs(pdf_path, backside_path, pdf_path)

    return {'output': output}
