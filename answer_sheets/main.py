"""
A common print resolution is 300 DPI, so for an 8.5 x 11-inch paper, the pixel dimensions would be 2550 x 3300 
pixels (8.5 inches * 300 DPI by 11 inches * 300 DPI).
"""

from PIL import Image, ImageDraw, ImageFont
import os
from myKwargs import MyKwargs
from rich.console import Console
import textwrap
import sys
import datetime
import json

console = Console()


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
        self.page_margins = kwargs.get("page_margins", (100, 100, 100, 100))

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
            self.font = ImageFont.truetype(self.font_path, 36)

        if self.font_bold:
            self.font_bold = ImageFont.truetype(self.font_bold, 36)

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
            [x, y - self.font_size_adj // 2],
            label,
            fill=fill,
            font=self.font,
        )

    def drawZebraLines(self, x, y):

        x = self.page_margins[1]
        y += self.line_spacing + self.bubble_height // 2 + 5
        w = (self.page_size[0] * self.dpi) - (
            self.page_margins[1] + self.page_margins[3]
        )
        h = self.bubble_height

        for i in range(self.num_questions):
            if i % 2 == 0:
                print(f"x:{x} y:{y} w:{w} h:{h}")
                self.addRectangle(x, y, w, h, color=(240, 240, 240), line=None)
            y += self.bubble_height + self.line_spacing

    def addBubble(self, x, y, line_thickness=2):
        x1 = x - (self.font_size_adj // 2)
        y1 = y - (self.font_size_adj // 2)
        x2 = x1 + self.bubble_width
        y2 = y1 + self.bubble_height

        if self.bubble_shape in ["circle", "ellipse"]:
            # Draw the circle with a specific fill color (e.g., 'red', 'blue', 'green', or an RGB tuple)

            self.draw.ellipse([x1, y1, x2, y2], outline="black", width=line_thickness)

        elif self.bubble_shape in ["rectangle", "square"]:

            self.draw.rectangle([x1, y1, x2, y2], outline="black", width=line_thickness)

    def addRectangle(self, x, y, w, h, color=(0, 0, 0), line=0):
        self.draw.rectangle([x, y, x + w, y + h], fill=color, outline=line)

        # draw.rectangle(rectangle_coordinates, fill=rectangle_color, outline=None)

    def drawTestNumBoxes(self, x, y, w, h, n=8):
        """
        Params:
            x (int) : startx
            y (int) : starty
            w (int) : rectangle width
            h (int) : rectangle height
            n (int) : number of boxes
        """

        self.draw.text(
            [x - 300, y],
            "Test Number: ",
            fill=(0, 0, 0),
            font=self.font_bold,
        )

        for _ in range(n):
            self.addRectangle(x, y, w, h, (0, 0, 0), 2)
            x += w

    def drawSignatureLine(self, x, y):

        self.draw.text(
            [x, y],
            "Signature: ",
            fill=(0, 0, 0),
            font=self.font_bold,
        )
        self.addRectangle(x + 300, y + 50, 500, 3, (0, 0, 0), 2)

    def addAnswerBubbles(self, start_x, start_y):
        '''
        TODO: right align question numbers. When brought into 
            triple digits the alignment of answer bubbles is not lining up
        
        TODO: add horizontal check for last column. 
            change bubble_size, column_width dynamically to ensure a fit for number 
            of questions requested by params. 
            currently being placed outside of bound of paper.

        TODO: determine width of single character and add it to self.column_width whenever
            the generated question number reaches 100 (n)
        '''
        x = start_x
        y = start_y

        i = 0  # Overall count for number of circles placed
        n = 1  # Question number

        if self.zebra_shading:
            self.drawZebraLines(x, y)

        option_set_width = (self.bubble_width + self.answer_spacing) \
                * self.num_ans_options + self.column_width

        while n <= self.num_questions:
            if i % self.num_ans_options == 0:
                label = f"{n:>3}."

            
                # dynamically adjust spacing based on the length of the question number
                label_width = len(label) * (self.font_size_adj // 2)  # Estimate label width
                label_bubble_spacing = 10  # Minimum spacing between label and first bubble
                
                # check if starting a new column is needed only when new answer is being created
                if y + self.bubble_height > self.img_height - self.page_margins[2]:
                    start_x += option_set_width + self.label_spacing  # Shift to next column
                    x = start_x
                    y = start_y

                # add question number
                self.addBubbleLabel(x, y, label) 
                x += label_width + label_bubble_spacing

            # add answer choice
            self.addBubble(x, y)
            answer_label = chr((i % self.num_ans_options) + 65)  # A, B, C, etc.
            self.addBubbleLabel(x - (label_bubble_spacing/2), y, answer_label, (200, 200, 200))
            
            # increment x to place the next answer choice if need be. 
            x += self.bubble_width + self.answer_spacing
            
            # check to see if we placed all options for this question. 
            if (i + 1) % self.num_ans_options == 0:
                x = start_x
                y += self.bubble_height + self.line_spacing
                n += 1

            i += 1


    def generate(self):
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
        self.drawSignatureLine(1350, 100)
        self.pasteImage(
            self.img_width // 2 - self.logo_image.width // 2, 50, self.logo_image
        )
        self.addAnswerBubbles(right, top)

    def saveImage(self, outPath=None, outName=None, show=False):
        # Save the image
        print("saving...")
        # self.final_image = Image.alpha_composite(self.image, self.overlay)
        if outPath is None:
            outPath = self.outPath
        if outName is None:
            outName = self.outName
        name = os.path.join(outPath, outName)

        print(f"{name}.png")
        self.image.save(f"{name}.png")
        #self.image.save(f"{name}.pdf")
        # self.image.show()


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
    question_counts = [20, 30, 50, 75, 100, 125, 150, 175, 200, 250]

    for count in question_counts:
        console.print(get_params("docs.json"))

        info = {
            "page_size": (8.5, 11),
            "img_align_path": "./assets/images/checkerboard_144x_adj_color.jpg",
            "logo_path": "./assets/images/LiveTestLogo_144x.png",
            "num_ans_options": 5,
            "num_questions": count,
            "dpi": 288,
            "font_size": 13,
            "bubble_shape": "circle",
            "bubble_size": 12,
            "bubble_ratio": 1,
            "font_path": "./assets/fonts/RobotoMono-Regular.ttf",
            "font_bold": "./assets/fonts/RobotoMono-Bold.ttf",
            "page_margins": (300, 100, 100, 50),
            "line_spacing": 10,
            "answer_spacing": 6,
            "label_spacing": 5,
            "zebra_shading": True,
            "label_style": None,
            "que_ident_style": None,
            "font_alpha": 50,
            "outPath": "./generatedSheets",
            "outName": None,
        }

        pictron = Pictron(**info)
        pictron.generate()
        pictron.saveImage()
