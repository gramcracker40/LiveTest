'''
This module was implemented to extract a Scantron form 882E from an image
Tested on 150 samples and got a 97% accuracy, 
see test_isolate_document to test it

Inconsistent backgrounds can affect the accuracy greatly. 
Inconsistent lighting can also play a role but usually doesn't thanks to dilation. 
See test_data/ALL for example images.
'''
import cv2
import numpy as np
from ScantronProcessor import show_image


class DocumentExtractionFailedError(Exception):
    """
    Exception raised for errors in the Scantron extraction process.
    """
    def __init__(self, 
        message="""Scantron extraction failed, 
please check the background and ensure 
there is a consistent background"""):
        self.message = message
        super().__init__(self.message)


def four_point_transform(image, pts):
    # order the points before passing to four_point_transform
    rect = np.array(pts, dtype="float32")
    (tl, tr, br, bl) = rect
    
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    return warped


def find_points_positions(points):
    '''
    accepts an np.array, finds the 5 points and their positions.
    consistently grabs the correct points for transformation.
    returns --> top left, top right, bottom right, bottom left most, bottom left second
    '''
    points = points.reshape(-1, 2)
    # sort points based on their Y-coordinate
    points_sorted_by_y = points[np.argsort(points[:, 1])]

    top_points = points_sorted_by_y[:2]  # grab the top two for the top points
    bottom_points = points_sorted_by_y[2:]  # last three points are bottom points

    top_left = min(top_points, key=lambda x: x[0])
    top_right = max(top_points, key=lambda x: x[0])

    # sort the bottom points based on their X-coordinate to distinguish left from right
    bottom_points_sorted_by_x = sorted(bottom_points, key=lambda x: x[0])
    bottom_left_most = bottom_points_sorted_by_x[0]
    bottom_left_second = bottom_points_sorted_by_x[1]
    bottom_right = bottom_points_sorted_by_x[2]

    return top_left, top_right, bottom_right, bottom_left_most, bottom_left_second


def pre_process(image):
    '''
    prepares the image for finding contours. 
    '''
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blur, 75, 200)
    kernel = np.ones((5, 5), np.uint8)
    dilated = cv2.dilate(edged, kernel, iterations=2)

    return dilated


def isolate_document(image_path:str=None, image_bytes:bytes=None):
    if image_path is not None:
        image = cv2.imread(image_path)
    elif image_bytes is not None:
        image_array = np.frombuffer(image, dtype=np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    else:
        raise ScantronExtractionFailedError("Must provide a valid image")
    
    dilated = pre_process(image)

    # find contours and sort in descending order based off area
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:3]

    # loop over the contours, find the document. 
    #   enforce 5 vertices in the resulting docCnt - document contour
    #   the start and end epsilon repeatedly approximate the polygon, 
    #  .02 epsilon will basically always approx a rectangle
    start_epsilon = 0.006  # start of epsilon range
    end_epsilon = 0.012    # end of epsilon range
    epsilon_interval = 0.001  # interval for each iteration

    docCnt = None
    for c in contours:
        peri = cv2.arcLength(c, True)
        for epsilon in np.arange(start_epsilon, end_epsilon, epsilon_interval):
            approx = cv2.approxPolyDP(c, epsilon * peri, True)
            if len(approx) == 5:
                docCnt = approx
                break
        if docCnt is not None:
            cv2.drawContours(image, [docCnt], -1, (255, 0, 0), 2)

    if docCnt is not None:
        tl, tr, br, bl1, bl2 = find_points_positions(np.array(docCnt))
        print(f"br: {br}\nbl1: {bl1}")
        br[1] = bl1[1]
        print(f"br: {br}\nbl1: {bl1}")
        transformed = four_point_transform(image, [tl, tr, br, bl1])
        
        # see stats to determine if it was successful or not
        height, width = transformed.shape[:2]
        dimension = height/width
        if dimension > 2.3 and dimension < 2.7:
            return transformed
        else:
            raise ScantronExtractionFailedError("""failed to extract Form 882E, please ensure the background is consistent and no lighting is distoring the view""")
    else:
        raise ScantronExtractionFailedError("No Scantron was found in the image")


# print(f"tl: {tl}\ntr: {tr}\nbr: {br}\nbl1: {bl1}\nbl2: {bl2}")

# print(f"sorted_pts: {sorted_pts}")
#     top_left = sorted_pts[0]
#     top_right = sorted_pts[1]
#     bottom_right = sorted_pts[-1]
#     bottom_left_first = sorted_pts[2]  
#     additional_vertex = sorted_pts[3]

#     ordered_pts = np.array([top_left, top_right, bottom_right, bottom_left_first], dtype="float32").reshape(4, 2)
#     additional_vertices = np.array([additional_vertex], dtype="float32") 

#     print(f"Points before passing: {[top_left[0], top_right[0], bottom_right[0], additional_vertex[0]]}")

#     print(f"ordered_pts: {ordered_pts}")
#     print(f"additional_vertices: {additional_vertices}")


# def extract_contour_area(image, contour):
#     mask = np.zeros(image.shape[:2], dtype=np.uint8)
#     # fill the mask with white in the area defined by the scantron
#     cv2.fillPoly(mask, [contour], 255)
#     # use the mask to isolate the scantron area
#     extracted_area = cv2.bitwise_and(image, image, mask=mask)
#     return extracted_area, mask


# def crop_to_contour(extracted_area, mask):
#     # find the bounding box of the contour from the mask
#     x, y, w, h = cv2.boundingRect(mask)
#     # crop the image to this bounding box
#     cropped_image = extracted_area[y:y+h, x:x+w]
#     return cropped_image



#  Random code from testing 

# # Apply a perspective transform to isolate the document
#     def order_points(pts):
#         # Initial ordering of the points: top-left, top-right, bottom-right, bottom-left
#         rect = np.zeros((4, 2), dtype="float32")
#         s = pts.sum(axis=1)
#         rect[0] = pts[np.argmin(s)]
#         rect[2] = pts[np.argmax(s)]
#         diff = np.diff(pts, axis=1)
#         rect[1] = pts[np.argmin(diff)]
#         rect[3] = pts[np.argmax(diff)]
#         return rect



# extracted_area, mask = extract_contour_area(image, docCnt)
#         # show_image("Extracted Area", extracted_area)
#         cropped_image = crop_to_contour(extracted_area, mask)
#         # show_image("Cropped Image", cropped_image)


# def merge_closest_points(points):
#     # Function to merge the closest two points in a set of five points
#     min_distance = float('inf')
#     pair_to_merge = (0, 1)

#     for i in range(len(points)):
#         for j in range(i + 1, len(points)):
#             distance = np.linalg.norm(points[i] - points[j])
#             if distance < min_distance:
#                 min_distance = distance
#                 pair_to_merge = (i, j)

#     # Merge the closest pair of points
#     merged_point = (points[pair_to_merge[0]] + points[pair_to_merge[1]]) / 2
#     new_points = [p for idx, p in enumerate(points) if idx not in pair_to_merge]
#     new_points.append(merged_point)

#     return np.array(new_points, dtype="float32")
    

# TESTING 
# Print contour areas and vertices
# for count, contour in enumerate(contours):
#     area = cv2.contourArea(contour)
#     peri = cv2.arcLength(contour, True)
#     approx = cv2.approxPolyDP(contour, 0.004 * peri, True)
#     print(f"Contour {count}: Area = {area}, Vertices = {len(approx)}")
# Draw all contours for analysis
# cv2.drawContours(image, contours, -1, (0, 255, 0), 2)



# def rotate_image(image, angle):
#     h, w = image.shape[:2]
#     center = (w // 2, h // 2)
#     M = cv2.getRotationMatrix2D(center, angle, 1.0)
#     rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
#     return rotated
    


# Example usage of find_points_positions
# contour = np.array([
#     [[100, 200]],  # Example point [X, Y]
#     [[150, 50]],
#     [[250, 100]],
#     [[200, 300]],
#     [[50, 250]],
# ])

# top_left, top_right, bottom_right, bottom_left_most, bottom_left_second = find_special_points(contour)

# print("Top Left:", top_left)
# print("Top Right:", top_right)
# print("Bottom Right:", bottom_right)
# print("Bottom Left Most:", bottom_left_most)
# print("Bottom Left Second:", bottom_left_second)
