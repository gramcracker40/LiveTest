import os
import glob
import cv2
from isolate_document import \
    isolate_document, show_image, ScantronExtractionFailedError
from find_answers import crop_to_answers, \
    draw_vertical_lines_from_start_percentage, \
    draw_horizontal_lines_from_start_percentage, \
    detect_answers, \
    find_markings, \
    find_gray_contours
    

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
            gray_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
            show_image('Gray Image', gray_image, w=500, h=800)
            ret, thresh = cv2.threshold(gray_image, 140, 255, cv2.THRESH_BINARY)
            show_image('Binary Thresholding', thresh, w=500, h=800)
            #find_gray_contours(cropped_image)
            #find_markings(cropped_image)
            #detect_answers(cropped_image)
            # draw_vertical_lines_from_start_percentage(cropped_image,14, 17.33)
            # draw_horizontal_lines_from_start_percentage(cropped_image, 2.3, 2.064)
            # show_image('Image with Horizontal/vertical Lines', cropped_image, h=1500)
            # To save the image, uncomment the following line and provide a save path
            # cv2.imwrite("path_to_save_directory/" + os.path.basename(image_path), isolated_document)
        except ScantronExtractionFailedError:
            print(f"Could not extract scantron --> {image_path}")

if __name__ == "__main__":
    # Replace 'path_to_directory' with the path to your directory containing images
    batch_process_documents('../../answer_sheets/generatedSheets/')

