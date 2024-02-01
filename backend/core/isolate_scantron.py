import cv2
import numpy as np
from ScantronProcessor import show_image

def merge_closest_points(points):
    # Function to merge the closest two points in a set of five points
    min_distance = float('inf')
    pair_to_merge = (0, 1)

    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            distance = np.linalg.norm(points[i] - points[j])
            if distance < min_distance:
                min_distance = distance
                pair_to_merge = (i, j)

    # Merge the closest pair of points
    merged_point = (points[pair_to_merge[0]] + points[pair_to_merge[1]]) / 2
    new_points = [p for idx, p in enumerate(points) if idx not in pair_to_merge]
    new_points.append(merged_point)

    return np.array(new_points, dtype="float32")


def four_point_transform(image, pts):
    # order the points before passing to four_point_transform
    (tl, tr, br, bl) = pts
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
    M = cv2.getPerspectiveTransform(pts, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    return warped

def extract_contour_area(image, contour):
    # Create a mask with the same dimensions as the image, initially all zeros (black)
    mask = np.zeros_like(image)
    # Fill the mask with white on the area defined by the contour
    cv2.fillPoly(mask, [contour], (255, 255, 255))
    # Bitwise-AND to isolate the contour area
    extracted_area = cv2.bitwise_and(image, mask)
    return extracted_area


def isolate_document(image_path):
    image = cv2.imread(image_path)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blur, 75, 200)
    kernel = np.ones((5, 5), np.uint8)
    dilated = cv2.dilate(edged, kernel, iterations=2)

    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:3]

    # TESTING 
    # Print contour areas and vertices
    # for count, contour in enumerate(contours):
    #     area = cv2.contourArea(contour)
    #     peri = cv2.arcLength(contour, True)
    #     approx = cv2.approxPolyDP(contour, 0.004 * peri, True)
    #     print(f"Contour {count}: Area = {area}, Vertices = {len(approx)}")
    # Draw all contours for analysis
    # cv2.drawContours(image, contours, -1, (0, 255, 0), 2)


    # Loop over the contours, find the document. 
    #   enforce 5 vertices through looping  the start and end epsilon
    start_epsilon = 0.006  # Start of epsilon range
    end_epsilon = 0.012    # End of epsilon range
    epsilon_interval = 0.001  # Interval for each iteration

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
            # return extract_contour_area(image, docCnt)
    # document is extracted perfectly need to arrange the 5 points now
    show_image("contours", image)

    sorted_pts = np.array(docCnt)
    print(f"sorted_pts: {sorted_pts}")
    top_left = sorted_pts[0]
    top_right = sorted_pts[-1]
    bottom_right = sorted_pts[-2]
    # Assuming the bottom vertices are always the last three in sorted order
    bottom_left_first = sorted_pts[1]  # First on the bottom left
    additional_vertex = sorted_pts[2]  # The one to exclude

    ordered_pts = np.array([top_left, top_right, bottom_right, bottom_left_first], dtype="float32").reshape(4, 2)
    additional_vertices = np.array([additional_vertex], dtype="float32")  # Stored for analysis

    print(f"ordered_pts: {ordered_pts}")
    print(f"additional_vertices: {additional_vertices}")
    # Proceed with your processing, e.g., extracting the contour area
    extracted_area = extract_contour_area(image, docCnt.reshape(-1, 1, 2))
    show_image("Extracted Area", extracted_area)

    # Get the isolated document
    return four_point_transform(image, ordered_pts)

if __name__ == "__main__":
    # Replace 'path_to_image.jpg' with your image file
    isolated_document = isolate_document("../../test_data/FakeTest3/KEY1.png")
    cv2.imshow("Isolated Document", isolated_document)
    cv2.waitKey(0)
    cv2.destroyAllWindows()









#  Code for working with 4 vertice contours. 

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

