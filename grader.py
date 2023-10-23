import numpy as np
import cv2
from imutils.perspective import four_point_transform
from imutils import contours
import imutils

examples = [
    "real_examples/IMG_4162.jpg", "real_examples/IMG_4163.jpg",
    "real_examples/IMG_4164.jpg", "real_examples/IMG_4165.jpg"
]


# only 4164 works in the current code.
# need to figure out the differences...
def process_image(image_path:str, threshold1, threshold2): 
    '''
    Description: Preprocesses the image to the point of the answers 
        being fully cropped from the scantron

    #TODO --> # it is finding the largest box within the scantron not the scantron itself...
        #      I do not know why it 
        # 	is not finding the scantron as a valid contour and using it as the largest...
        #   example IMG: 4164 is working but 4163, 4162, 4165 are not. They are grabbing the
        #   box inside the scantron and not the scantron itself. 4164 however is running as intended. 

        # thoughts:   We may be able to find some kind of contour completion algorithm 

    '''
    image = cv2.imread(image_path)
    desired_width = 700
    desired_height = 800

    if image is None:
        print("Image not loaded or does not exist.")
        return 0

    # gamma = 0.01

    # # Apply gamma correction to the image - helps with lights/shading
    # adjusted_image = np.power(image / 255.0, gamma).astype('float32') * 255.0
    # # Continue with image processing
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 

    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    # cv2.imshow(f"{image_path} blurred", blurred) 
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    blurred = cv2.convertScaleAbs(blurred)
    edged = cv2.Canny(blurred, threshold1, threshold2)

    edged_resized = cv2.resize(edged, (desired_width, desired_height))

    cnts, hierarchy = cv2.findContours(edged,  
        cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) 

    # we can assume that the scantron itself will be the contour with the largest area. 
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    print(f"{image_path} --> Area of largest contour: {cv2.contourArea(cnts[0])}")
    return cv2.contourArea(cnts[0])

    # # If a largest contour with the maximum area is found, you can proceed
    #     # You can now work with the largest area contour
    #     # For example, you can draw it on the original image
    # print(len(cnts))
    # print(cnts[0])
    # cv2.drawContours(image, cnts, -1, (0, 255, 0), 2)
        
    # # Display or save the original image with the largest area contour highlighted
    # resized_image = cv2.resize(image, (desired_width, desired_height))
    # cv2.imshow(f'{image_path} largest_contour_marked', resized_image) 
    # cv2.waitKey(0) 
    # cv2.destroyAllWindows() 


threshold1 = 0
threshold2 = 50 

    
for iter in range(300):
    print(f"\n\nthreshold1 = {threshold1} , threshold2 = {threshold2}")
    for example in examples:

        largest = process_image(example, threshold1, threshold2)

        print(f"{example} --> Area of largest contour: {largest}")

    threshold1 += 1
    threshold2 += 1