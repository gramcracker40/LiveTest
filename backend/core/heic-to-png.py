import os
from PIL import Image
import pyheif

def convert_heic_to_png(input_path, output_path):
    # Open the HEIC file
    heif_file = pyheif.read(input_path)

    # Convert HEIC to RGB
    image = Image.frombytes(
        heif_file.mode, 
        heif_file.size, 
        heif_file.data,
        "raw",
        heif_file.mode,
        heif_file.stride,
    )

    # Save as PNG
    output_file = os.path.join(output_path, os.path.splitext(os.path.basename(input_path))[0] + ".png")
    image.save(output_file, format="PNG")

def convert_all_heic_to_png(input_directory, output_directory):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
        print("Here 1")

    # Convert each HEIC file to PNG
    for heic_file in os.listdir(input_directory):
        input_path = os.path.join(input_directory, heic_file)
        convert_heic_to_png(input_path, output_directory)
        print(f"Converting --> {heic_file}")

if __name__ == "__main__":
    input_directory = 'TestData/BatchOne/'
    output_directory = 'TestData/BatchOne/'

    convert_all_heic_to_png(input_directory, output_directory)