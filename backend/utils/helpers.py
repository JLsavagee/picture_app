from PIL import ImageFont, Image, ImageDraw
from PyPDF2 import PdfWriter, PdfReader
import os

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
    
    temp_image = Image.new('RGBA', (1, 1), (255, 255, 255, 0))
    temp_draw = ImageDraw.Draw(temp_image)
    name_bbox = temp_draw.textbbox((0, 0), name, font=name_font)
    surname_bbox = temp_draw.textbbox((0, 0), surname, font=surname_font)
    
    name_width, name_height = name_bbox[2] - name_bbox[0], name_bbox[3] - name_bbox[1]
    surname_width, surname_height = surname_bbox[2] - surname_bbox[0], surname_bbox[3] - surname_bbox[1]
    space_width = temp_draw.textbbox((0, 0), ' ', font=name_font)[2] - temp_draw.textbbox((0, 0), ' ', font=name_font)[0]

    total_width = name_width + space_width + surname_width

    while total_width > 700 and name_font.size > 10 and surname_font.size > 10:
        name_font = ImageFont.truetype(name_font.path, name_font.size - 1)
        surname_font = ImageFont.truetype(surname_font.path, surname_font.size - 1)
        name_width = get_text_width(temp_draw, name, name_font)
        surname_width = get_text_width(temp_draw, surname, surname_font)
        total_width = name_width + space_width + surname_width

    max_height = max(name_height, surname_height)

    padded_width = total_width + 50
    padded_height = max_height + 50
    text_image = Image.new('RGBA', (padded_width, padded_height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(text_image)

    bottom_y = padded_height - 25

    name_y = bottom_y - name_height
    draw.text((25, name_y), name, font=name_font, fill=fill)
    
    surname_y = bottom_y - surname_height
    draw.text((25 + name_width + space_width, surname_y), surname, font=surname_font, fill=fill)

    rotated_text_image = text_image.rotate(angle, expand=True)

    new_x = x 
    new_y = y 

    image.paste(rotated_text_image, (new_x, new_y), rotated_text_image)

def merge_pdfs(pdf1_path, pdf2_path, output_pdf_path):
    reader1 = PdfReader(pdf1_path)
    reader2 = PdfReader(pdf2_path)
    writer = PdfWriter()

    for page in reader1.pages:
        writer.add_page(page)

    for page in reader2.pages:
        writer.add_page(page)

    with open(output_pdf_path, 'wb') as f:
        writer.write(f)

def clear_output_directory(output_folder):
    try:
        for filename in os.listdir(output_folder):
            file_path = os.path.join(output_folder, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
        print(f"Cleared all files in {output_folder}")
    except Exception as e:
        print(f"Error clearing output directory: {e}")

