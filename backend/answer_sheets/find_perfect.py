import cv2
import numpy as np

class DocumentExtractionFailedError(Exception):
    pass

def show_image(title: str, matlike: cv2.Mat_TYPE_MASK, w=600, h=700):
    """
    given a title and Matlike image, display it given configured width and height
    """

    temp = cv2.resize(matlike, (w, h))
    cv2.imshow(title, temp)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def pre_process(image):
    '''
    prepares the image for finding contours. 
    '''
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    kernel = np.ones((5, 5), np.uint8)
    dilated = cv2.dilate(thresh, kernel, iterations=2)

    return dilated

def order_points(pts):
    # Order points in the order: top-left, top-right, bottom-right, bottom-left
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect

def four_point_transform(image, pts):
    rect = order_points(pts)
    (tl, tr, br, bl) = rect
    maxWidth = max(int(np.linalg.norm(br - bl)), int(np.linalg.norm(tr - tl)))
    maxHeight = max(int(np.linalg.norm(tr - br)), int(np.linalg.norm(tl - bl)))

    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]],
        dtype="float32")

    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    return warped

def isolate_document(image_path:str=None, image_bytes:bytes=None):
    if image_path is not None:
        image = cv2.imread(image_path)
        print("Image loaded from path.")
    elif image_bytes is not None:
        image_array = np.frombuffer(image_bytes, dtype=np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        print("Image decoded from bytes.")
    else:
        raise DocumentExtractionFailedError("Must provide a valid image")

    image = pre_process(image)

    contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:3]
    print(f"Found {len(contours)} contours.")

    cv2.drawContours(image, contours, -1, (0,255,0), 6)
    show_image("contours detected", image)

    # Loop over the contours
    for i, c in enumerate(contours):
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        print(f"Contour #{i + 1}: {len(approx)} vertices.")

        if len(approx) == 4:
            print("Document found. Performing transformation.")
            transformed = four_point_transform(image, approx.reshape(4, 2))
            return transformed

    raise DocumentExtractionFailedError("Document could not be isolated")

# Example usage
# transformed_image = isolate_document(image_path='path_to_image.jpg')
# or
# transformed_image = isolate_document(image_bytes=binary_data_of_image)

# Example usage
transformed_image = isolate_document(image_path='submissionSheets/100-4/IMG_9338.png')
show_image("extracted image", transformed_image)
# or
# transformed_image = isolate_document(image_bytes=binary_data_of_image)
