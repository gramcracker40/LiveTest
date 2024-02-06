import os
import glob
from isolate_document import \
    isolate_document, show_image, ScantronExtractionFailedError
from find_answers import crop_to_answers
from find_numbers import detect_numbers_from_image

def batch_process_documents(directory):
    # Check if the directory exists
    if not os.path.exists(directory):
        print("Directory does not exist.")
        return

    # Get all image files in the directory
    image_files = glob.glob(os.path.join(directory, "*.png"))  # Add other image formats if needed

    # Process each image
    for image_path in image_files:
        try:
            print(f"Processing {image_path}...")
            isolated_document = isolate_document(image_path)
            show_image(f"Isolated Document {image_path}", isolated_document)
            cropped_image = crop_to_answers(isolated_document)  # Example: Crop to 80% of both width and height
            show_image('Cropped Image', cropped_image, w=500, h=800)
            found_numbers = detect_numbers_from_image(cropped_image)
            show_image('Numbers found', cropped_image, w=500, h=800)

            # To save the image, uncomment the following line and provide a save path
            # cv2.imwrite("path_to_save_directory/" + os.path.basename(image_path), isolated_document)
        except ScantronExtractionFailedError:
            print(f"Could not extract scantron --> {image_path}")


# Replace 'path_to_directory' with the path to your directory containing images
batch_process_documents('../../test_data/ALL/')

