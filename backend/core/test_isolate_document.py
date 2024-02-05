# /mnt/data/batch_document_isolation.py
import cv2
import os
import glob
from isolate_document import isolate_document, show_image  # Ensure this module is in the same directory

def batch_process_documents(directory):
    # Check if the directory exists
    if not os.path.exists(directory):
        print("Directory does not exist.")
        return

    # Get all image files in the directory
    image_files = glob.glob(os.path.join(directory, "*.png"))  # Add other image formats if needed

    # Process each image
    for image_path in image_files:
        print(f"Processing {image_path}...")
        isolated_document = isolate_document(image_path)
        # Display the isolated document
        show_image(f"Isolated Document {image_path}", isolated_document)
        
        # To save the image, uncomment the following line and provide a save path
        # cv2.imwrite("path_to_save_directory/" + os.path.basename(image_path), isolated_document)

# Replace 'path_to_directory' with the path to your directory containing images
batch_process_documents('../../test_data/ALL/')

