'''
Handles all processing to do with the Scantron form 882E
'''
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
    given an image of a form 882E scantron, handle all processing involved to get
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

                # Rotate the image
                M = cv2.getRotationMatrix2D(
                    (self.image.shape[1] / 2, self.image.shape[0] / 2),
                    180 + angle + 90,
                    1,
                )
                self.image = cv2.warpAffine(
                    self.image, M, (self.image.shape[1], self.image.shape[0])
                )

    def detect_answers(self, num_questions:int):
        '''
        takes resized image and finds the shaded in rectangle.
        starts by gray scaling image and then cropping the image to the answers section
        Takes an adaptive threshold to allow for semi rectangular human made marks can 
        be detected. It then finds the contours and runs the 
        
        also finds not answered.
        '''
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        # Determine the ROI boundaries
        h, w = gray.shape
        left_bound = int(0.15 * w)
        right_bound = int(0.58 * w)

        # Crop the image to the answers
        roi = gray[:, left_bound:right_bound]

        # Threshold the cropped image with adaptive thresholding, more leniance with handmade rectangles
        _, thresh = cv2.threshold(roi, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        #show_image("thresh", thresh) # shows the threshold version of the scantron
        # Detect contours in cropped section
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        filled_rectangles = []
        for contour in contours:
            # Get the bounding rectangle of the contour
            x, y, w, h = cv2.boundingRect(contour)

            # Aspect ratio to determine if the contour is horizontal rectangle
            aspect_ratio = float(w) / h

            # Filtering conditions: Aspect ratio allow shadings to be interpreted as rectangles. 
            if 650 < cv2.contourArea(contour) < 5000 and 1.1 < aspect_ratio < 7:
                filled_rectangles.append(
                    (x + left_bound, y, w, h)
                )  # Adjust x-coordinate considering the cropped image

        # Sort by vertical position
        filled_rectangles.sort(key=lambda r: r[1])
        # remove any extra markings in beginning
        filled_rectangles = filled_rectangles[len(filled_rectangles) - num_questions:]\
            if len(filled_rectangles) > num_questions else filled_rectangles

        # determine blanks/unmarked answers if any by measuring the
        # average y distance between found answers
        last_y = filled_rectangles[0][1] - 60 # relative starting point for 882E
        distances = [66] # prevent null division in mean
        self.not_answered = []
        # draw the rectangles onto the shaded answers. and find unanswered 
        iter = 0
        for question_num in range(num_questions):
            x, y, w, h = filled_rectangles[iter]
            
            diff = y - last_y
            # print(f"{question_num}: y:{y}, last_y:{last_y}, diff: {diff}, mean: {np.mean(distances)}")
            last_y = y
            if diff >= 1.9 * np.mean(distances):
                self.not_answered.append(question_num + 1)
                continue
            else:
                distances.append(diff)
            
            iter += 1
        
        return filled_rectangles
    
    def calculate_grade(self, graded_results:dict) -> float:
        '''
        input: graded_results from grade_answers()
        returns: the float point average of the graded scantron. 
        ex: 66.7%
        '''
        return round(float(float(len([graded_results[x][0] for x in graded_results \
                    if graded_results[x][0] == True]))/len(self.key)), 2)

    def grade_answers(self, answers:dict) -> dict:
        '''
        input: answers, from find_scantrons_answers {1: "A", 2: "E", 3, "N/A"}
        returns: results -> {1: (True, B), 2: (False, E)}
        '''
        # Matches a question numbers answer to a specific 
        #   x1, x2 pair. We take the points x and add the width/2 to get middle point
        #   see which pair it is in between to determine their answer

        
        # ex : 1: (True, "A")
        results = {}

        # If the answer is the correct answer
        for answer_num in answers:
            if answers[answer_num] == self.key[answer_num]:
                results[answer_num] = (True, answers[answer_num])
                cv2.rectangle(self.image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            else: # record the incorrect answer and their choice. 
                results[answer_num] = (False, answers[answer_num])
        
        grade = self.calculate_grade(results)*100

        
        # Put the grade on the final version of self.image
        if grade < 70:   # red
            cv2.putText(self.image, f"{grade}%",
            (10, 270), cv2.FONT_HERSHEY_SIMPLEX, 8, (0, 0, 255), 8)
        elif grade < 85: # yellow
            cv2.putText(self.image, f"{grade}%",
            (10, 270), cv2.FONT_HERSHEY_SIMPLEX, 8, (255, 255, 0), 8)
        else: # > 85     # green
            cv2.putText(self.image, f"{grade}%",
            (10, 270), cv2.FONT_HERSHEY_SIMPLEX, 8, (0, 255, 0), 8)
        
        return results
    
    def find_scantrons_answers(self, detected_answers:dict, num_questions:int):
        '''
        given the students answers from detect_answers(). find the answered values
        return ex: {1: "A", 2: "C"}
        '''
        scantron_results = {}
        answer_x_pairs = {
            "A" : (262, 402),
            "B" : (403, 557), 
            "C" : (519, 690), 
            "D" : (660, 825),
            "E" : (804, 950)
        }
        # determine if they had extra markings to begin. 
        answers = detected_answers
        if num_questions < len(answers):
            answers = answers[len(answers) - num_questions:]

        # build the key --> {1: 'A', 2: 'C', 3: 'E'}
        iter = 0 
        for question_num in range(num_questions):
            x,y,w,h = answers[iter]
            # determine middle point of answer
            answered_middle = x + (w/2)

            if question_num + 1 in self.not_answered:
                scantron_results[question_num + 1] = "N/A"
                continue

            # find what they answered from answer_x_pairs
            for val in answer_x_pairs:
                if (answered_middle >= answer_x_pairs[val][0]
                 and answered_middle <= answer_x_pairs[val][1]
                ):
                    scantron_results[question_num + 1] = val
                    break
            
            iter += 1

        return scantron_results

    def process(self, saved_location:str="saved", save_graded:bool=False):
        '''
        returns: (graded, grade_points)

        graded: dictionary returned from self.grade_answers {1: (True, 'E'), 2: (False, 'C')}
        grade_points: the scantron's score
        '''
        # preprocessing of image - isolates the scantron - stretches the image vertically
        self.image = find_and_rotate(self.image_path)
        self.resize_image(1700, 4400) 

        # finding the shaded contours in scantron, recording answers based off contour position.
        answered = self.detect_answers(len(self.key))
        real_answers = self.find_scantrons_answers(answered, len(self.key))
        
        # grading the real_answers against the passed through key
        graded = self.grade_answers(real_answers)
        
        # saving a copy of the scantrons processed form
        self.save_image(saved_location) if save_graded else None

        return (graded, self.calculate_grade(graded))



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

    processor = ScantronProcessor("../TestData/BatchOne/KEY1/IMG_8751", key)
    flipped = processor.rotate_to_orthogonal()
    flipped.save_image("")

    graded_results, grade = processor.process(saved_location=f"Graded-Located", save_graded=True)
    print(f"graded_results: {json.dumps(graded_results, indent=2)}\n grade: {grade*100}")
