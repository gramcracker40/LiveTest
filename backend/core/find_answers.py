'''
built as the second step in the Scantron grading system
runs after the document has been isolates using isolate_document.py
'''
import easyocr, cv2, re
from isolate_document import show_image
import numpy as np

def crop_to_answers(image, left=0.145, right=0.58, top=0.155, bottom=0.94):
    """
    crop a Matlike image (cv2) given a left, right, top, bottom bound
    default: crops to scantrons answers
    """
    height, width = image.shape[:2]
    cropped = image.copy()

    left_bound = int(left * width)
    right_bound = int(right * width)

    top_bound = int(top * height)
    bottom_bound = int(bottom * height)

    return cropped[top_bound:bottom_bound, left_bound:right_bound]


def detect_answers(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    # show_image("thresh", thresh) # shows the threshold version of the scantron
    # Detect contours in cropped section
    contours, _ = cv2.findContours(
        thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    filled_rectangles = []
    for contour in contours:
        # Get the bounding rectangle of the contour
        x, y, w, h = cv2.boundingRect(contour)

        # Aspect ratio to determine if the contour is horizontal rectangle
        aspect_ratio = float(w) / h
        print(f"aspect ratio: {aspect_ratio}\ncontourArea: {cv2.contourArea(contour)}")
        # Filtering conditions: Aspect ratio allow shadings to be interpreted as rectangles.
        if 200 > cv2.contourArea(contour) and 2.5 < aspect_ratio < 7:
            filled_rectangles.append(
                (x, y, w, h)
            ) 
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    show_image('answers_identified', image)


def draw_horizontal_lines_percentage(image, percentage_interval):

    # Get the image dimensions
    height, width = image.shape[:2]
    
    # Calculate the interval in pixels based on the percentage of the total height
    interval = int((percentage_interval / 100.0) * height)
    
    # Set the color of the line (BGR format)
    line_color = (0, 255, 0)  # Green
    
    # Set the thickness of the line
    line_thickness = 2
    
    # Draw horizontal lines across the image at the calculated interval
    for y in range(0, height, interval):
        start_point = (0, y)
        end_point = (width, y)
        cv2.line(image, start_point, end_point, line_color, line_thickness)
    
    # Display the result
    show_image('Image with Horizontal Lines', image)


def draw_vertical_lines_from_start_percentage(image, start_percentage, percentage_interval):
   
    # Get the image dimensions
    height, width = image.shape[:2]
    
    # Calculate the start position and interval in pixels based on percentages
    start_x = int((start_percentage / 100.0) * width)
    interval = int((percentage_interval / 100.0) * width)
    
    # Set the color of the line (BGR format)
    line_color = (0, 255, 0)  # Green
    
    # Set the thickness of the line
    line_thickness = 2
    
    # Draw vertical lines across the image starting from the calculated start position
    for x in range(start_x, width, interval):
        start_point = (x, 0)
        end_point = (x, height)
        cv2.line(image, start_point, end_point, line_color, line_thickness)
    
    # Display the result
    show_image('Image with Vertical Lines from Start Percentage', image)








# def check_range_1_50(text):
#     # Regular expression to match numbers 01 to 09, and 10 to 50
#     pattern = r'^([1-9]|[1-4][0-9]|50)$'
#     if re.match(pattern, text):
#         return True
#     return False



# def pre_process_ocr(image):
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#     # Apply Gaussian Blur to reduce noise
#     # clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))

#     _, trunc_threshold = cv2.threshold(gray, 190, 255, cv2.THRESH_TRUNC)

#     show_image("adaptive_thresh before OCR", trunc_threshold)
#     return trunc_threshold





















# def find_answer_numbers(image):
#     '''
#     find the answers 1-50
#     '''
#     image_copy = pre_process_ocr(image)
    
#     reader = easyocr.Reader(['en'])
#     results = reader.readtext(image_copy)

#     for (bbox, text, prob) in results:
#         print(f"Detected text: {text}, Confidence: {prob:.4f}")
#         # Print bounding box coordinates
#         print(f"Bounding box: {bbox}")

#     # display the image with bounding boxes around detected text
#     for (bbox, text, prob) in results:
#         top_left = tuple([int(val) for val in bbox[0]])
#         bottom_right = tuple([int(val) for val in bbox[2]])
#         cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)

#     return image
