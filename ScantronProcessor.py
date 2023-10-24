import cv2
import numpy as np
from imutils.perspective import four_point_transform
import json

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


def show_image(title, matlike, w=600, h=700):
    temp = cv2.resize(matlike, (w, h))
    cv2.imshow(title, temp)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


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
    '''
    given an image of a scantron, handle all processing involved to get
        the scantron graded. From plain user taken picture, all the way to 
        the graded outcome of the scantron. 
    '''

    def __init__(self, image_path:str, key:dict):
        self.image_path = image_path
        self.image = cv2.imread(self.image_path)
        self.processed_image = None
        self.key = key

    def resize_image(self, width, height):
        self.image = cv2.resize(self.image, (width, height)) 

    def save_image(self, save_name):
        cv2.imwrite(f"{self.image_path[:-4]}-{save_name}.jpg", self.image)

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

    def detect_answers(self):
        '''
        takes resized image and finds the shaded in rectangle.

        starts by gray scaling image and then cropping the image to the answers section
        '''
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        # Determine the ROI boundaries
        h, w = gray.shape
        left_bound = int(0.15 * w)
        right_bound = int(0.58 * w)

        # Crop the image to the answers
        roi = gray[:, left_bound:right_bound]
        show_image("roi", roi)
        # Threshold the cropped image
        _, thresh = cv2.threshold(roi, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        show_image("thresh", thresh)
        # Detect contours in cropped section
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        filled_rectangles = []
        for contour in contours:
            # Get the bounding rectangle of the contour
            x, y, w, h = cv2.boundingRect(contour)

            # Aspect ratio to determine if the contour is horizontal rectangle
            aspect_ratio = float(w) / h

            # Filtering conditions:
            if 500 < cv2.contourArea(contour) < 5000 and 1.0 < aspect_ratio < 7:
                filled_rectangles.append(
                    (x + left_bound, y, w, h)
                )  # Adjust x-coordinate considering the cropped image

        # Sort by vertical position
        filled_rectangles.sort(key=lambda r: r[1])

        # draw the rectangles onto the shaded answers. 
        for x, y, w, h in filled_rectangles:
            cv2.rectangle(self.image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            print(x, y)

        return filled_rectangles
    
    def grade_answers(self, answers:tuple) -> dict:
        '''
        input: answers, from detect_answers (detected shaded rectangles)
        returns: results -> {1: (True, B), 2: (False, E)}
        '''
        # Matches a question numbers answer to a specific 
        #   x1, x2 pair. We take the points x and add the width to get middle point
        #   see which pair it is mostly inside to determine their answer
        #   for that specific questions 
        
        # ex : 1: (True, "A")
        results = {}
        answer_x_pairs = {
            "A" : (262, 402),
            "B" : (403, 557), 
            "C" : (519, 690), 
            "D" : (660, 825),
            "E" : (804, 950)
        }
        # answers are rectangles from grade_answers
        for count, (x, y, w, h) in enumerate(answers):
            answered_middle = x + (w/2)
            
            # find what they answered
            for val in answer_x_pairs:
                if (answered_middle >= answer_x_pairs[val][0]
                 and answered_middle <= answer_x_pairs[val][1]
                ):
                    answer = val
                    break

            # If the answer is the correct answer
            if answer == self.key[count + 1]:
                results[count + 1] = (True, answer)
            else: # record the incorrect answer and their choice. 
                results[count + 1] = (False, answer)

        return results
    
    def calculate_grade(self, graded_results:dict) -> float:
        '''
        input: graded_results from grade_answers()
        returns: the float point average of the graded scantron. 
        ex: 66.7%
        '''
        return round(float(float(len([graded_results[x][0] for x in graded_results \
                    if graded_results[x][0] == True]))/len(graded_results)), 2)


    def process(self):
        # 1700/4400 defaults resize
        
        self.image = find_and_rotate(self.image_path)
        show_image("rotated image", self.image)
        
        self.resize_image(1700, 4400)

        # sorted 1-50 for all answered questions
        answered = self.detect_answers()
        self.save_image("answers-located")

        graded = self.grade_answers(answered)
        show_image("rectangles detected image", self.image) 

        print(json.dumps(graded, indent=2))
        
        print(f"Grade percentage: {self.calculate_grade(graded)}")
        print(f"Total answered: {len(answered)}")


if __name__ == "__main__":
    key = {
        1: 'C',
        2: 'E',
        3: 'C',
        4: 'E',
        5: 'C',
        6: 'C',
        7: 'D',
        8: 'C',
        9: 'D',
        10: 'C',
        11: 'D',
        12: 'B',
        13: 'C',
        14: 'A',
        15: 'C',
        16: 'B',
        17: 'C',
        18: 'A',
        19: 'B',
        20: 'C',
        21: 'A',
        22: 'A',
        23: 'C',
        24: 'D',
        25: 'C',
        26: 'B',
        27: 'B',
        28: 'C',
        29: 'E',
        30: 'A',
        31: 'C',
        32: 'B',
        33: 'D',
        34: 'D',
        35: 'E',
        36: 'C',
        37: 'C',
        38: 'C',
        39: 'C',
        40: 'B',
        41: 'C',
        42: 'B',
        43: 'D',
        44: 'B', 
        45: 'D'
    }

    processor = ScantronProcessor("real_examples/IMG_4165.jpg", key)
    processor.process()
