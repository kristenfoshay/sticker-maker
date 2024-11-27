from PIL import Image, ImageFilter
import numpy as np

def add_content_border(input_image, output_image, border_width=20, border_color='white'):
   
    border_width = max(3, border_width)
   
    img = Image.open(input_image)
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
   
    img_array = np.array(img)
   
    alpha = img_array[:, :, 3]
    content_mask = (alpha > 0).astype(np.uint8) * 255
   
    mask = Image.fromarray(content_mask)
   
    padded_size = (img.width + 2*border_width, img.height + 2*border_width)
    padded_mask = Image.new('L', padded_size, 0)
    padded_mask.paste(mask, (border_width, border_width))
   
    kernel_size = max(3, border_width * 2 + 1)
    outer_blur = padded_mask.filter(ImageFilter.GaussianBlur(radius=border_width))
    inner_blur = padded_mask.filter(ImageFilter.GaussianBlur(radius=max(1, border_width/2)))
   
    outer_arr = np.array(outer_blur)
    inner_arr = np.array(inner_blur)
   
    border_mask_arr = np.clip(outer_arr - inner_arr, 0, 255).astype(np.uint8)
    border_mask = Image.fromarray(border_mask_arr)
   
    border_image = Image.new('RGBA', padded_size, border_color)
    border_image.putalpha(border_mask)
   
    result = Image.new('RGBA', padded_size, (0, 0, 0, 0))
    result.paste(border_image, (0, 0), border_mask)
    result.paste(img, (border_width, border_width), img)
   
    result.save(output_image, 'PNG')
    print(f"Created content-aware border and saved to: {output_image}")

if __name__ == "__main__":
    add_content_border(
        input_image="dragonfly1.png",
        output_image="with_content_border4.png",
        border_width=350,
        border_color='white'
    )
