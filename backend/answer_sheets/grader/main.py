import cv2
import numpy as np

def detect_circles(image_path):
    # Read the image
    img = cv2.imread(image_path)
    if img is None:
        print("Error: Image cannot be loaded. Please check the path.")
        return

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur
    gray_blurred = cv2.GaussianBlur(gray, (9, 9), 2)

    # Detect circles using HoughCircles transform
    circles = cv2.HoughCircles(gray_blurred, cv2.HOUGH_GRADIENT, dp=1, minDist=20,
                               param1=50, param2=30, minRadius=0, maxRadius=0)

    if circles is not None:
        # Convert the (x, y) coordinates and radius of the circles to integers
        circles = np.uint16(np.around(circles))

        # Draw the circles in the original image
        for i in circles[0, :]:
            center = (i[0], i[1])
            radius = i[2]
            # Circle center
            cv2.circle(img, center, 1, (0, 100, 100), 3)
            # Circle outline
            cv2.circle(img, center, radius, (255, 0, 255), 3)

    # Display the image with detected circles
    cv2.imshow('Detected Circles', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Example usage
detect_circles('/home/bench/LiveTest/backend/answer_sheets/generatedSheets/perfTEST/5-choices/20-5-const.png')
