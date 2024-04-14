import cv2
import numpy as np

class OMRGrader:
    def __init__(self, num_choices, num_questions):
        self.num_choices = num_choices
        self.num_questions = num_questions

    def show_image(self, title: str, matlike, w=600, h=700):
        temp = cv2.resize(matlike, (w, h))
        cv2.imshow(title, temp)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def get_answer_bubbles(self, file_path:str=None, bytes_obj:bytes=None):
        if file_path is not None:
            image = cv2.imread(file_path)
        elif bytes_obj is not None:
            nparr = np.frombuffer(bytes_obj, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        else:
            raise ValueError("Either file_path or bytes_obj must be provided.")
        
        if image is None:
            raise ValueError("The image could not be loaded. Check the input data.")
        
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        self.thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

        self.show_image("Threshold", self.thresh)

        contours, _ = cv2.findContours(self.thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        question_contours = []

        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = w / float(h)
            if w >= 20 and h >= 20 and 0.9 <= aspect_ratio <= 1.1:
                question_contours.append(contour)

        return question_contours, image


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

        for contour, box in zip(cnts, bounding_boxes):
            if abs(box[1] - row_y) < 15:
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

        return rows


    def sort_rows_to_questions(self, rows):
        questions = {}
        col_num = 0
        i = 0
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

        returns --> answer-sheets recorded results. 


        '''
        answered = {}

        for question in questions:
            # start by sorting the contours from left to right for the question
            questions[question] = self.sort_contours(questions[question])
            bubbled = None

            for (j, c) in enumerate(questions[question]):
                # construct a mask that reveals only the current
                # "bubble" for the question
                mask = np.zeros(self.thresh.shape, dtype="uint8")
                cv2.drawContours(mask, [c], -1, 255, -1)
                # apply the mask to the thresholded image, then
                # count the number of non-zero pixels in the
                # bubble area
                mask = cv2.bitwise_and(self.thresh, self.thresh, mask=mask)
                total = cv2.countNonZero(mask)
                # if the current total has a larger number of total
                # non-zero pixels, then we are examining the currently
                # bubbled-in answer
                if bubbled is None or total > bubbled[0]:
                    bubbled = (total, j)
            
            # 0-6 num for A-G of the answer, the contour of the answer
            answered[question] = (bubbled[1], questions[question][bubbled[1]]) 

        return answered



    def run(self, file_path=None, bytes_obj=None):
        bubbles, image = self.get_answer_bubbles(file_path, bytes_obj)
        sorted_rows = self.group_bubbles_by_row(bubbles)
        questions = self.sort_rows_to_questions(sorted_rows)
        choices = self.identify_question_choices(questions)

        # Example visualization of specific questions
        highlight = sum((questions[q] for q in [67, 32, 45]), [])
        cv2.drawContours(image, highlight, -1, (0, 255, 0), 2)
        self.show_image("Questions Highlighted", image, w=1100, h=1900)


# Example usage
if __name__ == "__main__":
    grader = OMRGrader(num_choices=6, num_questions=100)
    grader.run(file_path='../generatedSheets/perfTEST/6-choices/100-6-const.png')
