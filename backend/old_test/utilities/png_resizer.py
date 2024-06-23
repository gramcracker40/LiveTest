from PIL import Image
import os

def resize_png_images(folder_path, target_size=1350000):
    for filename in os.listdir(folder_path):
        if filename.endswith('.png'):
            file_path = os.path.join(folder_path, filename)

            # Open the image and calculate new size
            with Image.open(file_path) as img:
                width, height = img.size
                aspect_ratio = width / height
                new_width = int((target_size ** 0.5) * aspect_ratio ** 0.5)
                new_height = int((target_size ** 0.5) / aspect_ratio ** 0.5)
                resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Save the resized image
            resized_img.save(file_path, optimize=True, quality=85)

folder_path = '../../../test_data/HEIC'
resize_png_images(folder_path)
