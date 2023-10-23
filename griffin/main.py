import cv2
import numpy as np


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
        return transformed
    return None


class ScantronProcessor:
    def __init__(self, image_path):
        self.image_path = image_path
        self.image = cv2.imread(self.image_path)
        self.processed_image = None

    def resize_image(self, width, height):
        self.image = cv2.resize(self.image, (width, height))

    def rotate_to_orthogonal(self):
        # Convert to grayscale
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        # Use Hough transform to detect lines
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)
        lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)

        if lines is not None:
            # Get the angle of the first line
            for rho, theta in lines[0]:
                # Convert the angle to degrees
                angle = (theta * 180) / np.pi - 90
                print(angle)
                # Rotate the image
                M = cv2.getRotationMatrix2D(
                    (self.image.shape[1] / 2, self.image.shape[0] / 2),
                    180 + angle + 90,
                    1,
                )
                self.image = cv2.warpAffine(
                    self.image, M, (self.image.shape[1], self.image.shape[0])
                )
        print(f"x: {self.image.shape[1]}, y:{self.image.shape[0]}")
        cv2.imshow("Detected Rectangles", self.image)
        cv2.waitKey(0)

    def crop_image(self, left_pct, right_pct):
        h, w, _ = self.image.shape
        left_bound = int(left_pct * w)
        right_bound = int(right_pct * w)
        self.image = self.image[:, left_bound:right_bound]

    def detect_filled_rectangles(self):
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        contours, _ = cv2.findContours(
            thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        filled_rectangles = []

        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = float(w) / h

            if 100 < cv2.contourArea(contour) < 3000 and 1.5 < aspect_ratio < 5:
                filled_rectangles.append((x, y, w, h))

        filled_rectangles.sort(key=lambda r: r[1])
        return filled_rectangles

    def process(self):
        self.resize_image(1700, 4400)
        self.rotate_to_orthogonal()
        self.crop_image(0.15, 0.42)
        cv2.imshow("Cropped Image", self.image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        return self.detect_filled_rectangles()


if __name__ == "__main__":
    # Example usage:
    # processor = ScantronProcessor("resized.jpg")
    processor = ScantronProcessor("IMG_4165.jpg")
    filled_rectangles = processor.process()
    print(filled_rectangles)
