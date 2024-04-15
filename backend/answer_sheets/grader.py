import cv2
import numpy as np
import os

class OMRGrader:
    def __init__(self, num_choices, num_questions):
        self.num_choices = num_choices
        self.num_questions = num_questions

    def show_image(self, title: str, matlike, w=600, h=700):
        temp = cv2.resize(matlike, (w, h))
        cv2.imshow(title, temp)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def is_circle(self, contour, threshold=0.9):
        area = cv2.contourArea(contour)
        
        # Calculate the bounding circle
        (x, y), radius = cv2.minEnclosingCircle(contour)
        circle_area = np.pi * (radius ** 2)
        
        # Calculate the circularity ratio
        circularity = area / circle_area
        
        # Return if the contour is a circle based on the threshold
        return circularity > threshold
    
    def get_answer_bubbles(self, file_path:str=None, bytes_obj:bytes=None):
        if file_path is not None:
            self.image = cv2.imread(file_path)
        elif bytes_obj is not None:
            nparr = np.frombuffer(bytes_obj, np.uint8)
            self.image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        else:
            raise ValueError("Either file_path or bytes_obj must be provided.")
        
        if self.image is None:
            raise ValueError("The image could not be loaded. Check the input data.")
        
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        self.thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

        self.show_image("Threshold", self.thresh)

        contours, _ = cv2.findContours(self.thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        question_contours = []

        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = w / float(h)
            if self.is_circle(contour) and 0.9 <= aspect_ratio <= 1.1:
                question_contours.append(contour)
                # cv2.drawContours(self.image, [contour], -1, (0,255,0), -1) # debugging

        self.show_image("Image", self.image)

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
        print(f"#ROWS: {len(rows)}, type(row): {type(rows[0])}")
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

        {}


        '''
        choices = {}
        for question, contours in questions.items():
            for j, c in enumerate(contours):
                print(f"Choice {j + 1} of question {question}: Type: {type(c)}, Shape: {c.shape}")

                mask = np.zeros_like(self.thresh, dtype="uint8")
                try:
                    cv2.drawContours(mask, [c], -1, 255, -1) 
                except cv2.error as e:
                    print(f"Error drawing contour {j} in question {question}: {e}")
                    continue 

                # apply the mask to the thresholded image, then count the number of non-zero pixels in the bubble area
                mask = cv2.bitwise_and(self.thresh, self.thresh, mask=mask)
                total = cv2.countNonZero(mask)
                print(f"#Non zero pixels: {total}")

                if question not in choices or total > choices[question][0]:
                    choices[question] = (total, c, chr(j + 65))  # store the choice with the highest total

        return choices
    

    def grade_choices(self, choices:dict, key:dict):
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
                cv2.drawContours(self.image, [choices[question_num][1]], -1, (0, 255, 0), -1)
                correct += 1
            else:
                graded[question_num] = False
                cv2.drawContours(self.image, [choices[question_num][1]], -1, (0, 0, 255), -1)

        return graded, correct/len(choices) * 100




    def run(self, file_path=None, bytes_obj=None, key:dict=None):
        '''
        helper function to execute the full functionality of the OMRGrader class in LiveTest

        returns:
            grade: int --> ex: 96 or 73
            graded: dict --> {1: False, 2: False, 3: True}
            choices: dict --> {1: (_, contour, chr(j + 65))}
        '''
        
        bubbles, image = self.get_answer_bubbles(file_path, bytes_obj)
        sorted_rows = self.group_bubbles_by_row(bubbles)
        questions = self.sort_rows_to_questions(sorted_rows)
        choices = self.identify_question_choices(questions)

        for question in choices:
            print(f"Question: {question}, Answer: {choices[question][2]}")

        graded, grade = self.grade_choices(choices, key)

        print(f"GRADE: {grade}\nGRADED: {graded}")
        
        self.show_image("Questions Highlighted", image, w=1100, h=1900)
        
        return grade, graded, choices

# usage
if __name__ == "__main__":
    num_choices = 6
    num_questions = 40

    grader = OMRGrader(
        num_choices=num_choices, 
        num_questions=num_questions
    )
    print(os.getcwd())
    grade, graded, choices = grader.run(
        file_path=f'generatedSheets/perfTEST/{num_questions}-{num_choices}-const.png', 
        key={
            "1": "F",
            "2": "D",
            "3": "A",
            "4": "E",
            "5": "A",
            "6": "A",
            "7": "D",
            "8": "D",
            "9": "C",
            "10": "F",
            "11": "B",
            "12": "F",
            "13": "D",
            "14": "C",
            "15": "D",
            "16": "E",
            "17": "F",
            "18": "E",
            "19": "C",
            "20": "D",
            "21": "B",
            "22": "E",
            "23": "B",
            "24": "C",
            "25": "F",
            "26": "C",
            "27": "B",
            "28": "F",
            "29": "C",
            "30": "F",
            "31": "E",
            "32": "B",
            "33": "B",
            "34": "D",
            "35": "B",
            "36": "E",
            "37": "D",
            "38": "C",
            "39": "D",
            "40": "C",
        }    
    )
    print(f"grade: {grade}\ngraded: {graded}\nchoices: {len(choices)}")
