### Testing out a basic one I found off the internet in a tutorial.


# import the necessary packages
#from imutils.perspective import four_point_transform
#from imutils import contours
import numpy as np
import argparse
import cv2

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="test_examples/answer_sheet.png")

args = vars(ap.parse_args())


# define the answer key
ANSWER_KEY = {0: 1, 1: 4, 2: 0, 3: 3, 4: 1}

image = cv2.imread(args["image"])

# Check if the image was loaded successfully
if image is None:
    print("Image not loaded or does not exist.")
else:
    # Continue with image processing
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 75, 200)


# # find contours in the edge map, then initialize
# # the contour that corresponds to the document
# cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
# 	cv2.CHAIN_APPROX_SIMPLE)
# cnts = imutils.grab_contours(cnts)
# docCnt = None
# # ensure that at least one contour was found
# if len(cnts) > 0:
# 	# sort the contours according to their size in
# 	# descending order
# 	cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
# 	# loop over the sorted contours
# 	for c in cnts:
# 		# approximate the contour
# 		peri = cv2.arcLength(c, True)
# 		approx = cv2.approxPolyDP(c, 0.02 * peri, True)
# 		# if our approximated contour has four points,
# 		# then we can assume we have found the paper
# 		if len(approx) == 4:
# 			docCnt = approx
# 			break


# # apply a four point perspective transform to both the
# # original image and grayscale image to obtain a top-down
# # birds eye view of the paper
# paper = four_point_transform(image, docCnt.reshape(4, 2))
# warped = four_point_transform(gray, docCnt.reshape(4, 2))


# # apply Otsu's thresholding method to binarize the warped
# # piece of paper
# thresh = cv2.threshold(warped, 0, 255,
# 	cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]


# # find contours in the thresholded image, then initialize
# # the list of contours that correspond to questions
# cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
# 	cv2.CHAIN_APPROX_SIMPLE)
# cnts = imutils.grab_contours(cnts)
# questionCnts = []
# # loop over the contours
# for c in cnts:
# 	# compute the bounding box of the contour, then use the
# 	# bounding box to derive the aspect ratio
# 	(x, y, w, h) = cv2.boundingRect(c)
# 	ar = w / float(h)
# 	# in order to label the contour as a question, region
# 	# should be sufficiently wide, sufficiently tall, and
# 	# have an aspect ratio approximately equal to 1
# 	if w >= 20 and h >= 20 and ar >= 0.9 and ar <= 1.1:
# 		questionCnts.append(c)