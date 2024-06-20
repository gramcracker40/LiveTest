"""
A common print resolution is 300 DPI, so for an 8.5 x 11-inch paper, the pixel dimensions would be 2550 x 3300 
pixels (8.5 inches * 300 DPI by 11 inches * 300 DPI).
"""

from PIL import Image, ImageDraw, ImageFont
import os
# from myKwargs import MyKwargs
from answer_sheets.myKwargs import MyKwargs

from rich.console import Console
import textwrap
import sys
import datetime
import json
import random

console = Console()

PRIMARY_CONFIG = {
    "page_size": (8.5, 11),
    "img_align_path": "answer_sheets/assets/images/checkerboard_144x_adj_color.jpg",
    "logo_path": "answer_sheets/assets/images/LiveTestLogo_144x.png",
    "bubble_shape": "circle",
    "bubble_ratio": 1,
    "font_path": "answer_sheets/assets/fonts/RobotoMono-Regular.ttf",
    "font_bold": "answer_sheets/assets/fonts/RobotoMono-Bold.ttf",
    "page_margins": (300, 100, 100, 50),
    "zebra_shading": False,
    "label_style": None,
    "que_ident_style": None,
    "font_alpha": 50,
    "outPath": "answer_sheets/generatedSheets/perfTEST",
    "outName": None,
}


def wrap_with_indent(text, width, indent):
    """
    Wrap text with indentation for lines after the first one.

    :param text: The text to wrap.
    :param width: The maximum width for each line.
    :param indent: The number of spaces to indent lines after the first one.
    :return: The wrapped text with indentation.
    """
    # Wrap the text
    wrapped_text = textwrap.fill(text, width=width)

    # print(wrapped_text)

    # Indent lines after the first one
    lines = wrapped_text.split("\n")
    indented_lines = [lines[0]] + [f"{' ' * indent}{line}" for line in lines[1:]]

    return "\n".join(indented_lines)


def wrap_docstring(obj):
    """
    Wrap a __doc__ string based on terminal width.

    :param obj: The object whose __doc__ string should be wrapped.
    :return: The wrapped __doc__ string.
    """
    terminal_width = os.get_terminal_size().columns
    docstring = obj.__doc__
    if docstring:
        wrapped_docstring = textwrap.fill(docstring, width=terminal_width)
        return wrapped_docstring
    else:
        return "No docstring available."


def find_longest_key(dictionary):
    """
    Find the longest key (by character length) in a dictionary.

    :param dictionary: The dictionary to search.
    :return: The longest key.
    """
    longest_key = max(dictionary.keys(), key=len)
    return longest_key


def get_params(fname="docs.json"):
    """ """

    with open(fname) as f:
        params = json.load(f)

    width = os.get_terminal_size().columns
    pad_keys = len(find_longest_key(params))
    pad_types = 7
    indent = pad_keys + pad_types + 3

    paramsString = ""

    for k, v in params.items():

        t = f"({v['type']})".ljust(pad_types, " ")
        d = v["description"]
        k = k.ljust(pad_keys, " ")

        d = wrap_with_indent(d, width - indent, indent)

        paramsString += f"[bold]{k}[/bold] [magenta]{t}[/magenta]: {d}\n"
    return paramsString


def open_image(image_path):
    # Check if the file exists
    if not os.path.exists(image_path):
        # If the file does not exist, raise FileNotFoundError
        raise FileNotFoundError(f"No such file: '{image_path}'")

    # If the file exists, open and return the image
    return Image.open(image_path)


def inchesToPixels(dpi, inches):
    """Given a size in inches, convert that to pixels based on dpi.

    Params:
        dpi (int) : dots per inch
        inches (int) : size in inches
    Returns:
        pixels (int) : inches converted to pixels
    """
    return int(dpi * inches)


def fontSizeToPixels(dpi, font_size):
    """Convert a font size like 12pt which is typically based on 72 dots per inch (dpi)
    to pixels based on another dpi like 300.
    1 inch * 300 DPI / 72 points per inch ≈ 417 points
    Params:
        dpi (int) : dots per inch
        font_size (int) : font_size based on 72 dpi
    Returns:
        pixels (int) : adjusted font_size
    """
    pixels = font_size * (dpi / 72)
    return int(pixels)


def generateName(num_questions, num_ans_options):
    timestamp = datetime.datetime.now().timestamp()
    return f"{num_questions}-{num_ans_options}-const"   # {int(timestamp)}


class Pictron:
    def __init__(self, **kwargs):
        """
        info = {
            "page_size": (8.5, 11),
            "img_align_path": "target_144x.png",
            "logo_path": "logo_144x.png",
            "num_ans_options": 5,
            "num_questions": 25,
            "dpi": 288,
            "font_size": 14,
            "bubble_shape": "square",
            "bubble_size": 12,
            "font_path": "./fonts/RobotoMono-Regular.ttf",
            "font_bold":"./fonts/RobotoMono-Bold.ttf",
            "page_margins": [300,100,100,100],
            "line_spacing": 20,
            "line_thickness": 3,
            "answer_spacing": 5,
            "label_spacing": 5,
            "zebra_shading": True,
            "label_style": None,
            "que_ident_style": None,
            "font_alpha": 50,
            "outPath":'./generatedSheets',
            "outName":None
        }
        """
        console.print(kwargs)

        # "label_style": None,
        # "que_ident_style": None,

        self.dpi = kwargs.get("dpi", 288)
        self.page_size = kwargs.get("page_size", (8.5, 11))
        self.bubble_size = kwargs.get("bubble_size", 15)
        self.bubble_ratio = kwargs.get("bubble_ratio", 1)
        self.bubble_shape = kwargs.get("bubble_shape", "circle")
        self.column_width = kwargs.get("column_width", 85)

        self.font_size = kwargs.get("font_size", 14)
        self.font_path = kwargs.get("font_path", None)
        self.font_bold = kwargs.get("font_bold", None)
        self.font_alpha = kwargs.get("font_alpha", 0)

        self.img_align_path = kwargs.get("img_align_path", None)
        self.logo_path = kwargs.get("logo_path", None)

        self.num_ans_options = kwargs.get("num_ans_options", 5)
        self.num_questions = kwargs.get("num_questions", 25)

        self.answer_spacing = kwargs.get("answer_spacing", 5)
        self.label_spacing = kwargs.get("label_spacing", 5)
        self.line_spacing = kwargs.get("line_spacing", 25)
        self.line_thickness = kwargs.get("line_thickness", 10)

        self.page_margins = kwargs.get("page_margins", (50, 50, 50, 50))

        self.zebra_shading = kwargs.get("zebra_shading", False)

        self.outPath = kwargs.get("outPath", "./generatedSheets")

        self.outName = kwargs.get("outName", None)

        if self.outName is None:
            self.outName = generateName(self.num_questions, self.num_ans_options)
        print(self.outName)

        self.img_width = inchesToPixels(self.dpi, self.page_size[0])
        self.img_height = inchesToPixels(self.dpi, self.page_size[1])

        self.font_size_adj = fontSizeToPixels(self.dpi, self.font_size)
        self.bubble_height = fontSizeToPixels(self.dpi, self.bubble_size)
        self.bubble_width = (
            fontSizeToPixels(self.dpi, self.bubble_size) * self.bubble_ratio
        )

        if self.font_path:
            self.font = ImageFont.truetype(self.font_path, self.font_size_adj)

        if self.font_bold:
            self.font_bold = ImageFont.truetype(self.font_bold, self.font_size_adj)

        # try:
        #     self.alignment_image = open_image(self.img_align_path)
        #     # Proceed with your operations on the image
        # except FileNotFoundError as e:
        #     print(e)

        try:
            self.alignment_image = open_image(self.img_align_path)
            # Proceed with your operations on the image
        except FileNotFoundError as e:
            print(e)

        try:
            self.logo_image = open_image(self.logo_path)
            # Proceed with your operations on the image
        except FileNotFoundError as e:
            print(e)

        self.logo_size = self.logo_image.size

        # Create a blank white image
        self.image = Image.new(
            "RGB", (self.img_width, self.img_height), (255, 255, 255)
        )

        self.draw = ImageDraw.Draw(self.image)

    @classmethod
    def find_best_config(self, num_questions:int, num_choices:int):
        '''
        class method to help find the best configuration for a range of questions and choices
          for the best looking version of Pictron from the default template engine. 
          num_questions: 0-200
          num_choices: 2-7

          returns: {primary_config | best_fitting_template}
        '''
        with open(f"answer_sheets/perfect_configs.json", "r") as conf_file:
            config_templates = json.load(conf_file)

        if num_questions <= 0 or num_questions > 200:
            return False

        templates = config_templates[str(num_choices)]
        template_counts = (10, 20, 30, 40, 50, 75, 100, 150, 200)
        template = 0

        for question_count in template_counts:
            if num_questions <= question_count:
                template = question_count
                break

        for temp in templates:
            if int(temp['num_questions']) == template:
                return temp | PRIMARY_CONFIG

    def pasteImage(self, x, y, img_obj):
        """ """

        # Overlay the image
        self.image.paste(img_obj, (x, y))

    def pasteAlignmentImages(self, positions=[]):
        for xy in positions:
            x, y = xy
            self.pasteImage(x, y, self.alignment_image)

    def addBubbleLabel(self, x, y, label, fill=(0, 0, 0)):
        # self.draw.text(
        #     [x, y - self.font_size_adj // 2], label, fill="black", font=self.font
        # )

        self.draw.text(
            [x + self.bubble_width // 6, y],
            label,
            fill=fill,
            font=self.font,
        )
    
    def addRectangle(self, x, y, w, h, color=(0, 0, 0), line=0):
        self.draw.rectangle([x, y, x + w, y + h], fill=color, outline=line)

        # draw.rectangle(rectangle_coordinates, fill=rectangle_color, outline=None)

    def drawZebraLines(self, x, y):

        x = self.page_margins[1]
        # y += self.line_spacing + self.bubble_height
        w = (self.page_size[0] * self.dpi) - (
            (self.page_margins[1] + self.page_margins[3]) // 2
        )
        h = self.bubble_height

        for i in range(self.num_questions):
            if i % 2 == 0:
                print(f"x:{x} y:{y} w:{w} h:{h}")
                self.addRectangle(x, y, w, h, color=(240, 240, 240), line=None)
            y += h

    def addBubble(self, x, y, line_thickness=2, filled:bool=False):
        x1 = x - (self.font_size_adj // 2)
        y1 = y - (self.font_size_adj // 2)
        x2 = x1 + self.bubble_width
        y2 = y1 + self.bubble_height

        if self.bubble_shape in ["circle", "ellipse"]:
            if filled:
                self.draw.ellipse([x1, y1, x2, y2], outline="black", width=line_thickness, fill="black")
            else:
                self.draw.ellipse([x1, y1, x2, y2], outline="black", width=line_thickness)

        elif self.bubble_shape in ["rectangle", "square"]:
            if filled:
                self.draw.rectangle([x1, y1, x2, y2], outline="black", fill="black")
            else:
                self.draw.rectangle([x1, y1, x2, y2], outline="black", width=line_thickness)
    
    def addRectangle(self, x, y, w, h, color=(0, 0, 0), line=0):
        self.draw.rectangle([x, y, x + w, y + h], fill=color, outline=line)

        # draw.rectangle(rectangle_coordinates, fill=rectangle_color, outline=None)

    def drawCourseTestName(self, course_name, test_name, x=650, y=35):
        """
        draw the course and test name on top of the answer sheet to make the answer sheet more unique

        Params:
            course_name (str)
            test_name (str)
            x (int) : startx
            y (int) : starty

        """
        courseTestFont = ImageFont.truetype(self.font_path, fontSizeToPixels(self.dpi, 12))

        self.draw.text(
            [x - 300, y],
            f"{course_name} : {test_name}",
            fill=(0, 0, 0),
            font=courseTestFont,
        )

        

    def drawSignatureLine(self, x, y):
        signatureLabelFont = ImageFont.truetype(self.font_path, fontSizeToPixels(self.dpi, 10))
        self.draw.text(
            [x, y],
            "Full Name: ",
            fill=(0, 0, 0),
            font=signatureLabelFont,
        )
        self.addRectangle(x + 300, y + 50, 500, 3, (0, 0, 0), 2)


    def addAnswerBubbles(self, start_x, start_y, randomize_filled:bool=False, answers:dict=None):
        '''
            build the answer sheets answer bubbles with the given settings set in the constructor. 
            
            start_x(int), start_y(int) = starting coordinates in pixels to start placing bubbles
            
            randomize_filled: bool --> we can also make the answer sheets in a way to have one of the answer 
            bubbles filled out already and a json file produced that records the 
            choice that was made. 

            answers: dict --> {1: 'A', 2:'E', 3:'C'}. For building a Test that has an established answer key. 

        TODO: add horizontal check for last column. 
            change bubble_size, column_width dynamically to ensure a fit for number 
            of questions requested by params. 
            currently being placed outside of bound of paper.

        '''
        x = start_x
        y = start_y

        i = 0  # Overall count for number of answer choices placed
        n = 1  # Question number

        # if self.zebra_shading:
        #     self.drawZebraLines(x, y)

        # 
        option_set_width = (self.bubble_width + self.answer_spacing) \
                * self.num_ans_options + self.column_width

        self.random_choices = {}

        # begin outputting answer choices
        while n <= self.num_questions:
            # check to see if we are on to the next question
            if i % self.num_ans_options == 0:
                # check if starting a new column is needed only when new answer is being created
                if y + self.bubble_height > self.img_height - self.page_margins[2]:
                    start_x += option_set_width + self.label_spacing  # Shift to next column
                    x = start_x
                    y = start_y

                question_label = f"{n:>3}"

                # if we are randomizing filled circles, choose the answer for this question here, save to random_choices
                if randomize_filled:
                    fill_answer = random.choice(range(self.num_ans_options))
                    self.random_choices[n] = chr(fill_answer + 65)
                # if we are generating an answer sheet for a test key, we may already have the key to generate as well. 
                elif type(answers) == dict:
                    vals = {"A": 0, "B": 1,  "C": 2, "D": 3, "E": 4, "F": 5, "G": 6}
                    fill_answer = vals[answers[n]] if n in answers else None
                    # print(f"fill_answer: {vals[answers[n]]}")
                # blank sheet meant for use in LiveTest
                else:
                    fill_answer = None

                # add question number to start off the new row
                self.addBubbleLabel(x - self.label_spacing, y, question_label) 

                # dynamically allocate necessary spacing between question number and first answer choice. 
                x += len(question_label) + ((self.font_size_adj // 2) * 3) + (self.bubble_width  // 2)

            # add answer choice - determine if it will be filled or not
            answer_label = chr((i % self.num_ans_options) + 65)  # A, B, C, etc.
            self.addBubble(x, y, filled=(i % self.num_ans_options) == fill_answer, line_thickness=self.line_thickness)
            self.addBubbleLabel(x, y, answer_label, (200, 200, 200)) \
                if (i % self.num_ans_options) != fill_answer else None
            
            # increment x to place the next answer_choice
            x += self.bubble_width + self.answer_spacing
            
            # check to see if we placed all answer choices for this question. 
            if (i + 1) % self.num_ans_options == 0:
                x = start_x
                y += self.bubble_height + self.line_spacing
                n += 1

            i += 1


    def generate(self, random_filled:bool=False, answers:dict=None, 
                 course_name:str=None, test_name:str=None):
        w, h = self.alignment_image.size
        positions = [
            (0, 0),
            (self.img_width - w, 0),
            (0, self.img_height - h),
            (
                self.img_width - w,
                self.img_height - h,
            ),
        ]

        top = self.page_margins[0]
        right = self.page_margins[3]

        self.pasteAlignmentImages(positions)
        self.drawCourseTestName(course_name, test_name) \
            if course_name is not None and test_name is not None else None
        self.drawSignatureLine(350, 130)
        self.pasteImage(
            180, 20, self.logo_image
        )
        self.addAnswerBubbles(right, top, randomize_filled=random_filled, answers=answers)
        

    def saveImage(self, outPath=None, outName=None, show=False):
        # Save the image
        print("saving...")
        # self.final_image = Image.alpha_composite(self.image, self.overlay)
        if outPath is None:
            outPath = self.outPath
        if outName is None:
            outName = self.outName
        self.name = outPath + '/' + outName

        print(f"{self.name}.png")
        self.image.save(f"{self.name}.png")
        
        #self.image.save(f"{name}.pdf")
        # self.image.show()

        # if self.random_choices != {}:
        #     with open(f"generatedSheets/answersJSON/{os.path.split(self.name)[-1]}.json", "w") as fp:
        #         json.dump(self.random_choices, fp, indent=True)


def usage():
    """
    Usage function for the custom scantron generator.

    [bold]Required Arguments[/bold]:
        questions=int          Number of questions (25, 50, 100, 200; default=50).
        options=int            Number of lettered options per question (default=7).

    [bold]Optional Arguments[/bold]:
        signature=bool         Include a signature line (default=True).
        test_id=bool           Include test ID boxes (default=True).
        info_location=str      Location for student info (top, left, right; default=top).
        border_size=float      Size of the checkerboard border in inches (.5 inches).
        check_size=float       Size of individual checks in the checkerboard in inches (default value recommended).
        logo_path=str          Path to an optional logo image file.
        header=str             Custom header text for the scantron.

    [bold]Example[/bold]:
        python script.py questions=100 options=5 signature=False test_id=True info_location=left border_size=0.5 check_size=0.1 logo_path=/path/to/logo.png header="Exam 101"

    Note: Boolean values can be passed as True/False.
    """
    wrapped = wrap_docstring(usage)
    console.print(wrapped)


def main():
    if len(sys.argv) < 2 or "-h" in sys.argv or "--help" in sys.argv:
        usage()
        sys.exit()

    # Your existing logic to parse arguments using MyKwargs or similar

    args, kwargs = MyKwargs(sys.argv)


def create_blank_image_with_overlay():
    # Create a blank white image of size 2550x3300
    blank_image = Image.new("RGB", (2550, 3300), "white")

    # Open the overlay image
    overlay_image = Image.open("checkerboard.png")

    # Calculate the position for the overlay image to be centered on the blank image
    overlay_size = overlay_image.size
    blank_size = blank_image.size
    position = (
        (blank_size[0] - overlay_size[0]) // 2,
        (blank_size[1] - overlay_size[1]) // 2,
    )

    # Paste the overlay image onto the blank image at the calculated position
    blank_image.paste(overlay_image, position, overlay_image)

    # Save the result as 'blank_with_overlay.png'
    blank_image.save("blank.png")


if __name__ == "__main__":
    # console.print(get_params(fname="docs.json"))
    # sys.exit()
    """
    1 Inch = 72px
    Params:
        page_size           (tuple): (int,int) (width,height) e.g. (8.5,11)
        img_align_path      (str): String path to alignment images for doc corners
        logo_path           (str): String path to the app logo
        num_ans_options     (int): Number of answer bubbles (A-?)
        num_questions       (int): Number of questions
        dpi                 (int): dots per inch used to convert fonts and inches to pixels
        font_size           (int): font size based on standard 72pt = inch
        bubble_shape        (str): [circle,ellipse,square,rectangle]
        bubble_size         (int): similar to font_size but gives options to adjust size within the class
        bubble_ratio        (float): Value to choose the width of a bubble if its an ellipse or rectangle (e.g 1.5 = 150% of height)
        font_path           (str): path to txt font
        font_bold           (str): path to bold txt font if any
        page_margins        (list): pixel size of any additional padding for [top,right,bottom,left]
        line_spacing        (int): pixel padding between lines of answers
        answer_spacing      (int): pixel padding between answer bubbles
        label_spacing       (int): pixel padding between label and bubble
        zebra_shading       (bool): Shade behind alternating lines? True / False
        label_style         (str): Style string for the A B C .... (tbd)
        que_ident_style     (str): Style string for the 1. 2. 3. .... (tbd)
    """
    question_counts = [150, 20, 50, 75]

    # perfTestCount = 1
    # perfTest = f"/generatedSheets/perfTEST/{perfTestCount}-choices"
    for count in question_counts:
        console.print(get_params("docs.json"))

        info = {
            "page_size": (8.5, 11),
            "img_align_path": "./assets/images/checkerboard_144x_adj_color.jpg",
            "logo_path": "./assets/images/LiveTestLogo_144x.png",
            "num_ans_options": 5,
            "num_questions": count,
            "font_size": 10,
            "bubble_shape": "circle",
            "bubble_size": 22,
            "bubble_ratio": 1,
            "font_path": "./assets/fonts/RobotoMono-Regular.ttf",
            "font_bold": "./assets/fonts/RobotoMono-Bold.ttf",
            "page_margins": (300, 100, 100, 50),
            "line_spacing": 20,
            "column_width": 70,
            "answer_spacing": 15,
            "label_spacing": 25,
            "zebra_shading": True,
            "label_style": None,
            "que_ident_style": None,
            "font_alpha": 50,
            "outPath": "./generatedSheets",
            "outName": None,
        }

        pictron = Pictron(**info)
        pictron.generate(random_filled=True)
        pictron.saveImage()
