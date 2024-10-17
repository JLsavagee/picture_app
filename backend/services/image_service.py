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

ASSETS_DIR = os.path.join(os.path.dirname(__file__), '..', 'utils', 'src', 'assets', 'fonts')

FIXED_PNG_PATH = os.path.join(os.path.dirname(__file__), '..', 'utils', 'src', 'assets', 'fixed_layers', 'Ellipse 1_Orange.png')
CAMP_LOGO_PNG_PATH = os.path.join(os.path.dirname(__file__), '..', 'utils', 'src', 'assets', 'fixed_layers', 'WLS_Logo.png')
#SPONSOR_LOGO_PNG_PATH = os.path.join(os.path.dirname(__file__), '..', 'utils', 'src', 'assets', 'fixed_layers', 'DominosLogo.png')

backside = os.path.join(os.path.dirname(__file__), '..', 'utils', 'src', 'assets', 'fixed_layers', 'rückseite.Sam&Sun.png')

# Transforming backside
backside_path = os.path.join(os.path.dirname(__file__), '..', 'utils', 'src', 'assets', 'fixed_layers', 'rückseite.Sam&Sun.pdf')
backside_img = Image.open(backside).convert("RGBA")
backside_img = backside_img.resize((BG_WIDTH, BG_HEIGHT), Image.LANCZOS)
backside_img.save(backside_path, format='PDF', resolution=300)

def generate_unique_filename(name, surname, output_dir):
    base_filename = f"{name}_{surname}"
    file_number = 1
    pdf_path = os.path.join(output_dir, f"{base_filename}_{file_number}.pdf")

    # Increment the number until a unique filename is found
    while os.path.exists(pdf_path):
        file_number += 1
        pdf_path = os.path.join(output_dir, f"{base_filename}_{file_number}.pdf")

    return pdf_path

def get_bounding_box(img):
    bbox = img.getbbox()
    return bbox

def remove_low_alpha_pixels(alpha_image, threshold=128):
    r, g, b, a = alpha_image.split()
    mask = a.point(lambda p: 255 if p>= threshold else 0)
    new_alpha = Image.composite(a, Image.new("L", alpha_image.size, 0), mask)
    alpha_image.putalpha(new_alpha)
    return alpha_image

def process_image(image_file_content, background_file_content, name, surname, position, trikotnummer):
    print(type(image_file_content))  # Should be bytes
    img = Image.open(io.BytesIO(image_file_content)).convert("RGBA")
    background = Image.open(io.BytesIO(background_file_content)).convert("RGBA")

    background = background.resize((BG_WIDTH, BG_HEIGHT), Image.LANCZOS)
    print("background size AND RUNNING: ", background)

    combined = background
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'output')

    #pdf_path_img = os.path.join(output_dir, f"{name}_{surname}.png")
    output_img = remove(img)
     
    cropped_output_img = remove_low_alpha_pixels(output_img, threshold=128)
    bbox = cropped_output_img.getbbox(alpha_only=True)
    alpha_bbox_output_img = output_img.crop(bbox)  
    #alpha_bbox_output_img.save(pdf_path_img, format='PNG', resolution=300) 

    #positioning the alpha_bbox trimmed image on the background
    # Margins
    left_right_margin = 1
    bottom_margin = 61
    top_margin = 69
    
    # Calculate the available width and height for the person image
    available_width = BG_WIDTH - 2 * left_right_margin
    available_height = BG_HEIGHT - bottom_margin - top_margin
    
    # Determine the scaling factor to fit the image within these dimensions
    person_width, person_height = alpha_bbox_output_img.size
    scale_factor_width = available_width / person_width
    scale_factor_height = available_height / person_height
    
    # Use the smaller scale factor to ensure the image fits within both width and height constraints
    scale_factor = min(scale_factor_width, scale_factor_height)
    
    # Resize the person image
    new_person_width = int(person_width * scale_factor)
    new_person_height = int(person_height * scale_factor)
    person_img_resized = alpha_bbox_output_img.resize((new_person_width, new_person_height))
    print("Person size: ", person_img_resized)
    
    # Calculate the position: align based on the bottom margin and centering horizontally
    x_position = (BG_WIDTH - new_person_width) // 2
    y_position = BG_HEIGHT - new_person_height - bottom_margin
    print("Position: ", x_position, y_position)
    
    # Create the final image
    final_image = combined.copy()
    final_image.paste(person_img_resized, (x_position, y_position), person_img_resized)
    # Now update 'combined' to reflect the image after positioning
    combined = final_image.copy()   


    #adding text and overlay layers
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

   # sponsor_logo_img = Image.open(SPONSOR_LOGO_PNG_PATH).convert("RGBA")
   # sponsor_logo_img.thumbnail((BG_WIDTH, BG_HEIGHT), Image.LANCZOS)
   # combined.paste(sponsor_logo_img, (490, 75), sponsor_logo_img)

    draw_rotated_text(combined, name, surname, name_font, surname_font, NAME_X, NAME_Y, -90)
    draw = ImageDraw.Draw(combined)
    draw_text(draw, position, position_font, POSITION_X, POSITION_Y)
    draw_text(draw, trikotnummer, trikotnummer_font, TRIKOTNUMMER_X, TRIKOTNUMMER_Y)

    output = io.BytesIO()
    combined.save(output, format='PNG')
    output.seek(0)

    
    os.makedirs(output_dir, exist_ok=True)
    pdf_path = generate_unique_filename(name, surname, output_dir)
    combined.save(pdf_path, format='PDF', resolution=300)

    merge_pdfs(pdf_path, backside_path, pdf_path)

    return {'pdf_path': pdf_path}
