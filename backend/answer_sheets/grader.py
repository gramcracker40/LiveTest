'''
This module implements the OMRGrader for the 
LiveTest answer_sheet module. So long as the answer
sheet stays within the below restrictions it will be able
to be graded. 

If you need an intro try running python grader.py
there is an example in the __main__ func below.
'''

import cv2
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os


class DocumentExtractionFailedError(Exception):
    """
    Exception raised for errors in the AnswerSheet extraction process.
    """
    def __init__(self, 
        message="""AnswerSheet extraction failed, 
please check the image and make sure that the Answer Sheet
is the main focus and takes up a majority of the screen. Also
take the time to level out the brightness levels."""):
        self.message = message
        super().__init__(self.message)


class AnswerBubbleIdentificationFailedError(Exception):
    def __init__(self, 
        message="""Question Choice Identification Failed,
This usually means we are able to isolate the document, 
but there are inconsistent backgrounds (brightness, non-solid) obstructing our 
strict normalization process. It could also mean that you are using the incorrect
template for this specific test. Please refer to the guide
on how to properly submit student answer sheets."""):
        self.message = message
        super().__init__(self.message)


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
    begins with a histogram equalization that will average out overly bright
    or dull images to help with glare and increases the contrast of the original image. 
    This significantly increases the identification rate of the answer sheets.
    
    We then perform a gaussian blur on the image to smooth it out and better connect the edges
    
    A threshold is then taken using OTSU's method, this automatically finds the optimum value. 
    We also invert the threshold to better identify the edges. 
    
    Finally we run Canny edge detection to grab the edges found in the image, this will identify the 
    edges for the answer sheet and returns an edge highlighted image. 
    
    Once we have the edges detected we dilate the image to further bring out the edges into the foreground
    This helps with splotchy background in removing background noise. 
    '''
    # image = equalize_histogram(image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    edges = cv2.Canny(thresh, 50, 150)
    kernel = np.ones((5, 5), np.uint8)
    dilated = cv2.dilate(edges, kernel, iterations=2)

    return dilated


def equalize_histogram(image):
    """
    Applies adaptive histogram equalization to the input image to improve contrast.
    
    Parameters:
    image (numpy.ndarray): Input image in BGR format.
    
    Returns:
    numpy.ndarray: Image after applying CLAHE.
    """
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Create a CLAHE object with a clip limit of 2.0 and a tile grid size of 8x8
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    
    # Apply CLAHE to the grayscale image
    equalized = clahe.apply(gray)
    
    # Convert the equalized grayscale image back to BGR format
    return cv2.cvtColor(equalized, cv2.COLOR_GRAY2BGR)


def order_points(pts):
    '''
    helper function for the four point transformation.
    Identifies the correct order of the vertices
    '''
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
    '''
    given four vertices of an identified rectangular contour
    perform a four point birds eye transformation of the answer sheet
    '''
    rect = order_points(pts)
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
        [0, maxHeight - 1]
    ], dtype="float32")

    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight), borderMode=cv2.BORDER_REPLICATE)
    # show_image("warped", warped)
    return warped


class OMRGrader:
    '''
    Handles all functionality surrounding grading LiveTest answer sheet documents
    
    can grade mechanically produced selected answers on LiveTest's answer_sheets module. 
        examples: ./generatedSheets

    can grade pictures taken of answer sheets filled out by hand as well. 
        examples: ./submissionSheets
        - handles all pre processing
        - handles four point transformation
        - returns Matlike obj of isolated answer sheets post four point transformation.
    
    See run() for the put together process
    '''
    def __init__(self, num_choices, num_questions, mechanical:bool=True, 
                 font_path:str="assets/fonts/RobotoMono-Regular.ttf", font_size:int=120):
        self.font_path = font_path
        self.font_size = font_size
        self.num_choices = num_choices
        self.num_questions = num_questions
        self.mechanical = mechanical

    @classmethod
    def convert_image_to_bytes(self, image: np.ndarray) -> bytes:
        if image is not None and image.size > 0:
            success, encoded_image = cv2.imencode('.png', image)
            if success:
                return encoded_image.tobytes()
        return None
    
    def show_image(self, title: str, matlike, w=600, h=700):
        temp = cv2.resize(matlike, (w, h))
        cv2.imshow(title, temp)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def is_circle(self, contour, threshold=0.83, epsilon_factor=0.01):
        '''
        Given a contour, determine if it is a circle using contour approximation and circularity ratio.
        '''
        # Approximate the contour
        epsilon = epsilon_factor * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        # Debugging: print the number of vertices of the approximated contour
        print(f"Approximated contour has {len(approx)} vertices")

        # Check if the approximated contour has enough vertices to be considered a circle
        if len(approx) < 8:
            return False

        area = cv2.contourArea(contour)

        # Bounding circle
        (x, y), radius = cv2.minEnclosingCircle(contour)
        circle_area = np.pi * (radius ** 2)

        # Circularity ratio
        circularity = area / circle_area

        # Debugging: print the area, circle area, and circularity
        print(f"Contour area: {area}, Circle area: {circle_area}, Circularity: {circularity}")

        # Return if the contour is a circle
        return circularity > threshold

    

    def isolate_document(self, image_path:str=None, image_bytes:bytes=None):
        if image_path is not None:
            image = cv2.imread(image_path)
            print("Image loaded from path.")
        elif image_bytes is not None:
            image_array = np.frombuffer(image_bytes, dtype=np.uint8)
            image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
            print("Image decoded from bytes.")
        else:
            raise DocumentExtractionFailedError("Must provide a valid image")
        self.image = image
        # show_image("prepre_process(image)", image)
        image_proc = pre_process(image)
        # show_image("pre_process(image)", image_proc)
        contours, _ = cv2.findContours(image_proc, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:3]
        print(f"Found {len(contours)} contours.")

        # cv2.drawContours(image, contours, -1, (0,255,255), 111)
        # show_image("drawContours(image)", image)

        # Loop over the contours
        for i, c in enumerate(contours):
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.025 * peri, True)
            print(f"Contour #{i + 1}: {len(approx)} vertices.")

            if len(approx) == 4:
                print("Document found. Performing transformation.")
                transformed = four_point_transform(image, approx.reshape(4, 2))
                # show_image("transformed!", transformed)
                return transformed

        raise DocumentExtractionFailedError("Document could not be isolated")


    def get_answer_bubbles(self, file_path:str=None, bytes_obj:bytes=None):
        if file_path is not None:
            print("file path ran")
            self.image = cv2.imread(file_path)
        elif bytes_obj is not None:
            print("bytes obj eing used")
            nparr = np.frombuffer(bytes_obj, np.uint8)
            self.image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            print("loaded image!")
        else:
            if not len(self.image) > 0:
                raise ValueError("Either file_path or bytes_obj must be provided.")
        
        if self.image is None:
            raise ValueError("The image could not be loaded. Check the input data.")
        # show_image("starting answer_bubbles", self.image)
        print("starting bubbles")
        if len(self.image.shape) == 3: # rectangle
            # self.image = equalize_histogram(self.image) # levels out inconsistent brightness
            # self.show_image("histogram equalized", self.image)
            gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            # self.show_image("grayed!", gray)
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            # self.show_image("blurred image", blurred)
            self.thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
            print("thresholded image!")
        # self.show_image("Thresholded image", self.thresh)

        contours, _ = cv2.findContours(self.thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        question_contours = []
        # print(f"contours: {len(contours)}")
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = w / float(h)
            if self.is_circle(contour): # and 0.91 <= aspect_ratio <= 1.09:
                question_contours.append(contour)
                # cv2.drawContours(self.image, [contour], -1, (0,255,0), 2) # debugging

        # # Perform validation check to make sure you have the right number of questions
        # if len(question_contours) / self.num_choices < self.num_questions:
        #     raise AnswerBubbleIdentificationFailedError()

        return question_contours, self.image


    def sort_contours(self, cnts, method="left-to-right"):
        reverse = method in ["right-to-left", "bottom-to-top"]
        i = 1 if method in ["top-to-bottom", "bottom-to-top"] else 0
        bounding_boxes = [cv2.boundingRect(c) for c in cnts]
        sorted_cnts = sorted(zip(cnts, bounding_boxes), key=lambda b: b[1][i], reverse=reverse)
        return zip(*sorted_cnts)


    def group_bubbles_by_row(self, cnts):
        cnts, bounding_boxes = self.sort_contours(cnts, "top-to-bottom")
        rows = []
        current_row = []
        row_y = bounding_boxes[0][1]
        row_threshold = 25  # You may want to adjust this threshold based on your specific requirements

        for contour, box in zip(cnts, bounding_boxes):
            if abs(box[1] - row_y) < row_threshold:
                current_row.append(contour)
            else:
                if current_row:
                    current_row, _ = self.sort_contours(current_row, "left-to-right")
                    rows.append(current_row)
                current_row = [contour]
                row_y = box[1]
        
        if current_row:
            current_row, _ = self.sort_contours(current_row, "left-to-right")
            rows.append(current_row)

        # TODO clean up repeated code
        template_counts = (10, 20, 30, 40, 50, 75, 100, 150, 200)
        template = 0

        for question_count in template_counts:
            if self.num_questions <= question_count:
                template = question_count
                break

        expected_num_contours = self.num_choices * template

        print(f"# question contours: {len(cnts)}  expected_num_contours: {expected_num_contours}")
        # TODO implement better solution?
        # Check if there are more question contours than expected
        if len(cnts) > expected_num_contours:
            # Remove the top row - it will be course/test name
            rows.pop(0)

        return rows


    def sort_rows_to_questions(self, rows):
        questions = {}
        col_num = 0
        i = 0
        # print(f"#ROWS: {len(rows)}, type(row): {type(rows[0])}")
        while i < self.num_questions:
            questions[i + 1] = [
                rows[i % len(rows)][choice]
                for choice in range(col_num, col_num + self.num_choices)
            ]
            i += 1
            if i % len(rows) == 0:
                col_num += self.num_choices

        return questions
    
    
    def identify_question_choices(self, questions:dict):
        '''
        questions: 
        {
            1: [[cntCoordinatesA], [cntCoordinatesB]], 
            2: [[cntCoordinatesA], [cntCoordinatesB]]
        }

        Description: given a dictionary of questions from sortRowsToQuestions, return a 
        dictionary with the same keys but the contour that is the marked answer
        as the value

        How it works: counting the number of non-zero pixels (foreground pixels) in each bubble region
                        this function determines which bubble was circled in out of the number of choices. 
        
        To determine where the blank markings are located, we keep track of the average
        non zero counts of each answer choice. So long as they mark the first few questions
        it works but it needs a more surefire solution. We could measure this value at blank-test-creation.

        returns --> answer-sheets recorded results. 
        {}
        '''
        choices = {}
        for question, contours in questions.items():
            for j, c in enumerate(contours):
                # print(f"Choice {j + 1} of question {question}: Type: {type(c)}, Shape: {c.shape}")

                mask = np.zeros_like(self.thresh, dtype="uint8")
                try:
                    cv2.drawContours(mask, [c], -1, 255, -1) 
                except cv2.error as e:
                    print(f"Error drawing contour {j} in question {question}: {e}")
                    continue 

                # apply the mask to the thresholded image, then count the number of non-zero pixels in the bubble area
                mask = cv2.bitwise_and(self.thresh, self.thresh, mask=mask)
                total = cv2.countNonZero(mask)
                #print(f"#Non zero pixels: {total}")

                # mark the selected answer
                if question not in choices or total > choices[question][0]:
                    choices[question] = (total, c, chr(j + 65))  # store the choice with the highest total

        return choices
    

    def grade_choices(self, choices:dict, key:dict, outline_thickness:int=10):
        '''
        given a key and a dict of choices { 1: (_, contour, 'B'), 2: (_, contour, 'E') } 
        return the grade for the answer sheet, as well as mark whether or not they got it right
        and return the graded version
        '''
        graded = {}
        correct = 0

        for question_num in choices:
            if choices[question_num][2] == key[str(question_num)]:
                graded[question_num] = True
                # draw green outline
                cv2.drawContours(self.image, [choices[question_num][1]], -1, (0, 255, 0), outline_thickness)
                correct += 1
            else:
                graded[question_num] = False
                # draw red outline
                cv2.drawContours(self.image, [choices[question_num][1]], -1, (0, 0, 255), outline_thickness)

        return graded, round(correct/len(choices) * 100, 2)


    def add_grade(self, image, grade, 
                color=(0, 0, 0), 
                output_size=(1920, 1080)):
        '''
        Add the grade to the top right of the graded answer sheet.
        '''
        
        # Convert Matlike to RGB
        cv_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Convert the OpenCV image to a PIL image
        pil_image = Image.fromarray(cv_image)
        
        # Resize the image
        pil_image = pil_image.resize(output_size)

        # Draw grade on PIL image
        draw = ImageDraw.Draw(pil_image)
        font = ImageFont.truetype(self.font_path, self.font_size)
        
        # Calculate the width and height of the text to be drawn
        text = f"{round(grade, 2)}%"
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        # Calculate the position to anchor the text at the top-right corner
        image_width, image_height = pil_image.size
        position = (image_width - text_width - 10, 10)  # 10 pixels padding from the edges

        # Draw the text on the image
        draw.text(
            xy=position,
            text=text,
            font=font,
            fill=color,
        )

        # Convert back to OpenCV image
        cv_image_final = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

        return cv_image_final


    def run(
            self, 
            file_path:str=None, 
            bytes_obj:bytes=None, 
            key:dict=None
            ) \
            -> tuple[float, dict, dict] | tuple[bool, bool, str]:
        '''
        helper function to execute the full functionality of the OMRGrader class in LiveTest
        uses configurations set in the constructor to grade the answer sheet. 

        returns:
            grade: int --> ex: 96 or 73
            graded: dict --> {1: False, 2: False, 3: True}
            choices: dict --> {1: (_, contour, chr(j + 65))}
        '''
        try:
            # determine if the run is on a mechanical or a real life image of a submission. 
            if not self.mechanical: # run the pre-processing method
                self.image = self.isolate_document(file_path, bytes_obj)
                bubbles, image = self.get_answer_bubbles()
            else:
                bubbles, image = self.get_answer_bubbles(file_path, bytes_obj)
            # print("got bubbles")
        except DocumentExtractionFailedError as err:
            return (False, False, err)
        except AnswerBubbleIdentificationFailedError as err:
            return (False, False, err)
        
        # start by grouping the question choices by rows
        sorted_rows = self.group_bubbles_by_row(bubbles)
        # once you have your rows, organize the rows into questions
        questions = self.sort_rows_to_questions(sorted_rows)
        # determine which of the answer choices were selected using OMR
        choices = self.identify_question_choices(questions)
        # using the provided key, grade the selected choices
        # marking wrong choices red and right choices green
        graded, grade = self.grade_choices(choices, key)

        # print(f"GRADE: {grade}\nGRADED: {graded}")
        # place a grade on the image that will change color based on their performance
        #grade_color = (255, 0, 0) if grade < 66 \
                #else (0, 255, 0) if grade >= 85 \
                #else (0, 255, 255) # yellow 70-84

        # add the grade to the image
        #self.image = self.add_grade(image, grade, color=grade_color)

        return grade, graded, choices

# usage
if __name__ == "__main__":
    num_choices = 4
    num_questions = 100

    grader = OMRGrader(
        num_choices=num_choices, 
        num_questions=num_questions, 
        mechanical=False
    )
    # print(os.getcwd())
    # f'generatedSheets/fakeTest{num_questions}-{num_choices}/submission-2.png'

    grade, graded, choices = grader.run(
        file_path=f"submissionSheets/100-4/IMG_9348.png", 
        key = { 
            '1': 'A',
            '2': 'B',
            '3': 'C',
            '4': 'D',
            '5': 'A',
            '6': 'B',
            '7': 'C',
            '8': 'D',
            '9': 'A',
            '10': 'B',
            '11': 'C',
            '12': 'D',
            '13': 'A',
            '14': 'B',
            '15': 'C',
            '16': 'D',
            '17': 'A',
            '18': 'B',
            '19': 'C',
            '20': 'D',
            '21': 'A',
            '22': 'B',
            '23': 'C',
            '24': 'D',
            '25': 'A',
            '26': 'B',
            '27': 'C',
            '28': 'D',
            '29': 'A',
            '30': 'B',
            '31': 'C',
            '32': 'D',
            '33': 'A',
            '34': 'B',
            '35': 'C',
            '36': 'D',
            '37': 'A',
            '38': 'B',
            '39': 'C',
            '40': 'D',
            '41': 'A',
            '42': 'B',
            '43': 'C',
            '44': 'D',
            '45': 'A',
            '46': 'B',
            '47': 'C',
            '48': 'D',
            '49': 'A',
            '50': 'B',
            '51': 'C',
            '52': 'D',
            '53': 'A',
            '54': 'B',
            '55': 'C',
            '56': 'D',
            '57': 'A',
            '58': 'B',
            '59': 'C',
            '60': 'D',
            '61': 'A',
            '62': 'B',
            '63': 'C',
            '64': 'D',
            '65': 'A',
            '66': 'B',
            '67': 'C',
            '68': 'D',
            '69': 'A',
            '70': 'B',
            '71': 'C',
            '72': 'D',
            '73': 'A',
            '74': 'B',
            '75': 'C',
            '76': 'D',
            '77': 'A',
            '78': 'B',
            '79': 'C',
            '80': 'D',
            '81': 'A',
            '82': 'B',
            '83': 'C',
            '84': 'D',
            '85': 'A',
            '86': 'B',
            '87': 'C',
            '88': 'D',
            '89': 'A',
            '90': 'B',
            '91': 'C',
            '92': 'D',
            '93': 'A',
            '94': 'B',
            '95': 'C',
            '96': 'D',
            '97': 'A',
            '98': 'B',
            '99': 'C',
            '100': 'D'
        }    
    )
    print(f"grade: {grade}\ngraded: {graded}\nchoices: {len(choices)}")
