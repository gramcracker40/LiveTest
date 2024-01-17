import cv2
import pytesseract
from ScantronProcessor import show_image

class AnswerSheetGrader:
    def __init__(self, img_path):
        self.img_path = img_path

    def pre_process_image(self):
        self.image = cv2.imread(self.img_path) if ".jpg" in self.img_path else \
            cv2.imread(self.img_path, cv2.IMREAD_COLOR) if ".png" in self.img_path else \
            None
        self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        _, self.thresh = cv2.threshold(self.gray, 150, 255, cv2.THRESH_BINARY_INV)
        self.contours, _ = cv2.findContours(self.thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.contours = sorted(self.contours, key=lambda ctr: cv2.boundingRect(ctr)[1])

    def find_numbers(self):
        for ctr in self.contours:
            # Get bounding box
            x, y, w, h = cv2.boundingRect(ctr)

            # Crop and recognize
            roi = self.thresh[y:y+h, x:x+w]
            text = pytesseract.image_to_string(roi, config='outputbase digits')
            print("Detected number:", text.strip())

            cv2.rectangle(self.image, (x, y), (x+w, y+h), (0, 255, 0), 2)

    def process(self):
        self.pre_process_image()
        self.find_numbers()
        show_image(self.image)


if __name__ == "__main__":
    test = AnswerSheetGrader("../../test_data/BatchOne/KEY1/IMG_8750.png")
    test.process()