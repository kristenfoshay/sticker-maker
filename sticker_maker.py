from PIL import Image, ImageFilter
import numpy as np

def add_content_border(input_image, output_image, border_width=20, border_color='white'):
    """
    Add a contour border around the actual content of a PNG image (non-transparent pixels).
   
    Args:
        input_image (str): Path to input image
        output_image (str): Path to save output image
        border_width (int): Width of the border in pixels
        border_color (str): Color of the border
    """
    # Ensure border_width is at least 3 pixels
    border_width = max(3, border_width)
   
    # Open and convert image to RGBA
    img = Image.open(input_image)
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
   
    # Convert to numpy array for easier manipulation
    img_array = np.array(img)
   
    # Create a binary mask of non-transparent pixels
    alpha = img_array[:, :, 3]
    content_mask = (alpha > 0).astype(np.uint8) * 255
   
    # Convert back to PIL Image
    mask = Image.fromarray(content_mask)
   
    # Create a new image with padding for the border
    padded_size = (img.width + 2*border_width, img.height + 2*border_width)
    padded_mask = Image.new('L', padded_size, 0)
    padded_mask.paste(mask, (border_width, border_width))
   
    # Create two differently blurred versions
    kernel_size = max(3, border_width * 2 + 1)  # Ensure odd kernel size
    outer_blur = padded_mask.filter(ImageFilter.GaussianBlur(radius=border_width))
    inner_blur = padded_mask.filter(ImageFilter.GaussianBlur(radius=max(1, border_width/2)))
   
    # Convert to numpy arrays for faster processing
    outer_arr = np.array(outer_blur)
    inner_arr = np.array(inner_blur)
   
    # Create border mask using numpy operations
    border_mask_arr = np.clip(outer_arr - inner_arr, 0, 255).astype(np.uint8)
    border_mask = Image.fromarray(border_mask_arr)
   
    # Create the border image
    border_image = Image.new('RGBA', padded_size, border_color)
    border_image.putalpha(border_mask)
   
    # Create the final image
    result = Image.new('RGBA', padded_size, (0, 0, 0, 0))
    result.paste(border_image, (0, 0), border_mask)
    result.paste(img, (border_width, border_width), img)
   
    # Save the result
    result.save(output_image, 'PNG')
    print(f"Created content-aware border and saved to: {output_image}")

# Example usage
if __name__ == "__main__":
    add_content_border(
        input_image="dragonfly1.png",
        output_image="with_content_border4.png",
        border_width=350,
        border_color='white'
    )
