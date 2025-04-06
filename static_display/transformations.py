import sys
import os
from PIL import Image,ImageDraw,ImageFont

def invert_colors(bitmap_image):
    """
    Inverts the colors of a 1-bit bitmap image.

    Args:
        bitmap_image (PIL.Image): The input bitmap image to be inverted.

    Returns:
        PIL.Image: The color-inverted bitmap image.
    """
    # Convert the image to '1' mode if it's not already
    if bitmap_image.mode != '1':
        bitmap_image = bitmap_image.convert('1')

    # Invert the image colors
    inverted_image = bitmap_image.point(lambda x: 255 - x)

    return inverted_image


def png_to_bmp(image_path, image_name):
    """
    Converts a PNG image to BMP format.

    Args:
        image_path (str): The path to the input PNG image.
        image_name (str): The name of the output BMP image.

    Returns:
        str: The path to the converted BMP image.
    """
    # Open the PNG image
    png_image = Image.open(os.path.join(image_path, image_name)).convert("RGBA")

    background = Image.new("RGBA", png_image.size, (255, 255, 255, 255))

    bitmap_image = Image.alpha_composite(background, png_image).convert('1')

    return bitmap_image

def on_raspi():
    """
    Check if the current device is a Raspberry Pi.

    Returns:
        bool: True if running on Raspberry Pi, False otherwise.
    """

    raspberry_pi = False
    if os.path.exists('/proc/device-tree/model'):
        with open('/proc/device-tree/model', 'r') as f:
            model = f.read().strip()
            if 'Raspberry Pi' in model:
                raspberry_pi = True
                print("Running on Raspberry Pi")
            else:
                print("Not running on Raspberry Pi")
    else:
        print("Not running on Raspberry Pi")

    return raspberry_pi