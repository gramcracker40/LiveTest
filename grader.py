import numpy as np
import cv2
from imutils.perspective import four_point_transform
from imutils import contours
import imutils

image = cv2.imread("real_examples/IMG_4163.jpg")
desired_width = 700
desired_height = 800

if image is None:
    print("Image not loaded or does not exist.")
else:
    # Continue with image processing
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 75, 200)

edged_resized = cv2.resize(edged, (desired_width, desired_height))
# cv2.imshow('edged', edged_resized) 
# cv2.waitKey(0) 
# cv2.destroyAllWindows() 

cnts, hierarchy = cv2.findContours(edged,  
    cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) 

# drawing all found contours on original image
# print("Number of Contours found = " + str(len(cnts))) 
  
# -1 signifies drawing all contours 
cv2.drawContours(image, cnts, -1, (0, 255, 0), 3) 

resized_image = cv2.resize(image, (desired_width, desired_height))
cv2.imshow('Contours', resized_image) 
cv2.waitKey(0) 
cv2.destroyAllWindows() 


# we can assume that the scantron itself will be the contour with the largest area. 
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
print(cv2.contourArea(cnts[0]))
largest_area = 0
for c in cnts:
    area = cv2.contourArea(c)
    
    # Check if the current contour has a larger area than the previously found largest contour
    if area > largest_area:
        largest_area = area
        largest_contour = c
        print(f"New largest found!\n  num: {largest_area}")

# If a largest contour with the maximum area is found, you can proceed
if largest_contour is not None:
    # You can now work with the largest area contour
    # For example, you can draw it on the original image
    cv2.drawContours(image, [largest_contour], -1, (0, 255, 0), 2)
    
	#TODO --> # it is finding the largest box within the scantron... I do not know why it 
	# 	is not finding the scantron as a valid contour and using it as the largest...


    
    # Apply a perspective transform to obtain a top-down view of the largest area contour
    # if len(largest_contour) >= 4:
    #     paper = four_point_transform(image, largest_contour.reshape(4, 2))
        
    # Show or save the transformed image (paper)

# Display or save the original image with the largest area contour highlighted
resized_image = cv2.resize(image, (desired_width, desired_height))
cv2.imshow('Contours', resized_image) 
cv2.waitKey(0) 
cv2.destroyAllWindows() 

