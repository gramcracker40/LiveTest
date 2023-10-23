import cv2
import numpy as np
import sys


def sort_vertices(vert):
    """
    Sort the given vertices of a quadrilateral based on their spatial positions.

    :param vert: List of vertices.
    :return: Sorted vertices in the order of [top-left, top-right, bottom-right, bottom-left].
    """
    vert = [v[0] for v in vert]
    top = sorted(vert, key=lambda x: x[1])[:2]
    bottom = sorted(vert, key=lambda x: x[1])[2:]
    tl, tr = sorted(top, key=lambda x: x[0])
    bl, br = sorted(bottom, key=lambda x: x[0])
    return np.array([tl, tr, br, bl], dtype="float32")


def four_point_transform(image, pts):
    """
    Perform a four point perspective transform on the given image.

    :param image: Input image to be transformed.
    :param pts: List of vertices defining the quadrilateral to be transformed.
    :return: Transformed image.
    """
    rect = sort_vertices(pts)
    (tl, tr, br, bl) = rect

    widthA = np.linalg.norm(br - bl)
    widthB = np.linalg.norm(tr - tl)
    heightA = np.linalg.norm(tr - br)
    heightB = np.linalg.norm(tl - bl)
    maxWidth = max(int(widthA), int(widthB))
    maxHeight = max(int(heightA), int(heightB))

    dst = np.array(
        [[0, 0], [maxWidth - 1, 0], [maxWidth - 1, maxHeight - 1], [0, maxHeight - 1]],
        dtype="float32",
    )

    print((maxWidth, maxHeight))

    M = cv2.getPerspectiveTransform(rect, dst)
    return cv2.warpPerspective(image, M, (maxWidth, maxHeight))


def find_and_rotate(image_path):
    """
    Detect a quadrilateral (like a paper sheet) in the image, then perform a perspective
    transform to make it upright and orthogonal.

    :param image_path: Path to the input image.
    :return: Transformed image if a quadrilateral is detected, else None.
    """
    # Read in the image and preprocess it
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 50, 150)

    # Dilation helps in connecting the edges
    kernel = np.ones((5, 5), np.uint8)
    dilated = cv2.dilate(edged, kernel, iterations=2)

    # Find contours and keep the largest one
    contours, _ = cv2.findContours(
        dilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    largest = max(contours, key=cv2.contourArea)

    # Get the approximation of the contour
    peri = cv2.arcLength(largest, True)
    vertices = cv2.approxPolyDP(largest, 0.02 * peri, True)

    if len(vertices) == 4:
        transformed = four_point_transform(image, vertices)
        print(transformed)
        return transformed
    return None


# def extract_cells(image):
#     # Convert to grayscale and threshold
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     _, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY_INV)

#     # Find contours
#     contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#     # Filter out very small and very large contours (noise and whole grid respectively)
#     contours = [cnt for cnt in contours if 200 < cv2.contourArea(cnt) < 1500]

#     return contours


# def compute_fill_percentage(contour, thresh_image):
#     mask = np.zeros(thresh_image.shape, dtype=np.uint8)
#     cv2.drawContours(mask, [contour], -1, 255, thickness=cv2.FILLED)
#     fill = np.sum(mask & thresh_image)
#     total = np.sum(mask / 255)
#     return fill / total


# def process_scantron(image_array):
#     # Since the image is already loaded, you don't need to read it again
#     thresh_image = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)
#     _, thresh_image = cv2.threshold(thresh_image, 120, 255, cv2.THRESH_BINARY_INV)

#     cells = extract_cells(image_array)

#     # Draw contours on a copy of the original image
#     vis_image = image_array.copy()
#     cv2.drawContours(vis_image, cells, -1, (0, 255, 0), 2)  # Drawing in green color

#     show_scantron("Extracted Cells", vis_image)

#     fill_percentages = [compute_fill_percentage(cell, thresh_image) for cell in cells]
#     for i, percent in enumerate(fill_percentages):
#         print(f"Cell {i + 1}: {percent * 100:.2f}% fill")


def show_scantron(title, array):
    cv2.imshow(title, array)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# def detect_filled_bubbles_v2(img, rows=50, cols=5):
#     """
#     Detect the filled bubbles in a scantron image.

#     Args:
#     - img (np.array): The pre-processed scantron image.
#     - rows (int): The number of questions/rows on the scantron.
#     - cols (int): The number of options per question.

#     Returns:
#     - list: A list of the detected answers (as characters).
#     """
#     # img = cv2.imread(img, cv2.IMREAD_GRAYSCALE)

#     img = cv2.imread(img)

#     # Convert the image to grayscale
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#     show_scantron("gray scale", gray)

#     # Threshold the image
#     _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

#     # Find the height and width of each cell (bubble area) by dividing the total height and width
#     cell_height, cell_width = binary.shape[0] // rows, binary.shape[1] // cols

#     print(cell_height, cell_width)

#     answers = []

#     for i in range(rows):
#         # Extract each row
#         row_start, row_end = i * cell_height, (i + 1) * cell_height
#         row = binary[row_start:row_end, :]

#         intensities = []
#         n = 1
#         for j in range(cols):
#             # Extract each column (bubble) within the row
#             col_start, col_end = j * cell_width, (j + 1) * cell_width
#             bubble = row[:, col_start:col_end]

#             # Compute the mean intensity of the bubble (lower value for filled bubbles)
#             intensities.append(np.mean(bubble))
#             print(f"{n}. {intensities}")
#             n += 1

#         # Find the bubble with the lowest intensity in the row (most filled)
#         filled_bubble_idx = np.argmin(intensities)
#         answers.append(chr(65 + filled_bubble_idx))

#     return answers


def detect_filled_rectangles(image_path):
    # Load the image and convert it to grayscale
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Determine the ROI boundaries
    h, w = gray.shape
    left_bound = int(0.15 * w)
    right_bound = int(0.58 * w)

    # Crop the image to the ROI
    roi = gray[:, left_bound:right_bound]

    # Threshold the cropped image
    _, thresh = cv2.threshold(roi, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Detect contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    filled_rectangles = []

    for contour in contours:
        # Get the bounding rectangle of the contour
        x, y, w, h = cv2.boundingRect(contour)

        # Aspect ratio to determine if the contour is horizontal rectangle
        aspect_ratio = float(w) / h

        # Filtering conditions:
        # - Consider contours with certain area to avoid noise
        # - Ensure the contour resembles a horizontal rectangle
        if 100 < cv2.contourArea(contour) < 3000 and 1.5 < aspect_ratio < 5:
            filled_rectangles.append(
                (x + left_bound, y, w, h)
            )  # Adjust x-coordinate considering the cropped image

    # Sort by vertical position
    filled_rectangles.sort(key=lambda r: r[1])

    return filled_rectangles


if __name__ == "__main__":
    # 1700 x 4400
    # To visualize the detected rectangles
    image_path = "resized.jpg"
    image = cv2.imread(image_path)
    rectangles = detect_filled_rectangles(image_path)
    for x, y, w, h in rectangles:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        print(x, y)

    # print(rectangles)

    cv2.imshow("Detected Rectangles", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
