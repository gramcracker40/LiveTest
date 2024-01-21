import cv2
import easyocr

# Create an OCR reader for English language
reader = easyocr.Reader(['en'])

image_path = "../../test_data/BatchOne/KEY1/IMG_8761.png"
image = cv2.imread(image_path)
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Use thresholding to get a binary image
_, binary_image = cv2.threshold(gray_image, 150, 255, cv2.THRESH_BINARY_INV)
# Find contours
contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Function to sort contours by their y-coordinate (top-to-bottom)
def sort_contours(cnts):
    boundingBoxes = [cv2.boundingRect(c) for c in cnts]
    cnts, boundingBoxes = zip(*sorted(zip(cnts, boundingBoxes), key=lambda b:b[1][1], reverse=False))
    return cnts

# Sort the contours
sorted_contours = sort_contours(contours)

# Initialize a list to store detected numbers
detected_numbers = []

# Loop over the sorted contours
for c in sorted_contours:
    # Get the bounding box of the contour
    (x, y, w, h) = cv2.boundingRect(c)
    
    # Make sure the contour area is not too small
    if w > 5 and h > 15:
        # Crop the image to the bounding box size
        roi = binary_image[y:y+h, x:x+w]
        
        # Convert the cropped image to a format suitable for EasyOCR
        roi = cv2.cvtColor(roi, cv2.COLOR_GRAY2BGR)

        # Use EasyOCR to convert image to string
        results = reader.readtext(roi)
        
        # Process results
        for (bbox, text, prob) in results:
            # Try to convert the detected text to an integer
            try:
                number = int(text.strip())
                if 1 <= number <= 50:
                    detected_numbers.append(number)
            except ValueError:
                pass

# Print the detected numbers
print("Detected numbers:", detected_numbers)
