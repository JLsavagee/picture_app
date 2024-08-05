import io
import os
from PIL import Image, ImageDraw, ImageFont, ImageOps
from rembg import remove
from backend.utils.helpers import load_font, draw_rotated_text, draw_text, merge_pdfs

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

def process_image(image_file, background_file, name, surname, position, trikotnummer, zoom_factor):
    zoom_factor = float(zoom_factor)
    img = Image.open(image_file.stream).convert("RGBA")
    background = Image.open(background_file.stream).convert("RGBA")

    background = background.resize((BG_WIDTH, BG_HEIGHT), Image.LANCZOS)

    output_img = remove(img)

    IMG_WIDTH = int(output_img.width / zoom_factor)
    IMG_HEIGHT = int(output_img.height / zoom_factor)

    IMG_POSITION_X = (BG_WIDTH - IMG_WIDTH) // 2
    IMG_POSITION_Y = (BG_HEIGHT - IMG_HEIGHT) // 2

    IMG_POSITION_Y -= 200

    output_img = ImageOps.fit(output_img, (IMG_WIDTH, IMG_HEIGHT), method=Image.LANCZOS, centering=(0.5, 0.5))

    combined = background.copy()
    combined.paste(output_img, (IMG_POSITION_X, IMG_POSITION_Y), output_img)

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
