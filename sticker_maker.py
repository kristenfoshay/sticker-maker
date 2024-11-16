from PIL import Image, ImageOps, ImageDraw
import os
from pathlib import Path

def create_sticker_outline(input_path, output_path, outline_width=20, outline_color='white', padding=40):

    img = Image.open(input_path)
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    total_padding = (outline_width + padding) * 2
    new_size = (img.width + total_padding, img.height + total_padding)
    new_img = Image.new('RGBA', new_size, (0, 0, 0, 0))
    
    paste_pos = (outline_width + padding, outline_width + padding)
    new_img.paste(img, paste_pos, img)
    
    alpha = new_img.split()[3]
    
    mask = ImageOps.expand(alpha, outline_width, fill=255)
    outline = Image.new('RGBA', new_size, outline_color)
    
    result = Image.composite(outline, new_img, mask)
    result.paste(new_img, (0, 0), new_img)
    
    result.save(output_path, 'PNG')

def process_folder(input_folder, output_folder, **keyword):

    Path(output_folder).mkdir(parents=True, exist_ok=True)
    
    for file in os.listdir(input_folder):
        if file.lower().endswith('.png'):
            input_path = os.path.join(input_folder, file)
            output_path = os.path.join(output_folder, f'sticker_{file}')
            create_sticker_outline(input_path, output_path, **keyword)
