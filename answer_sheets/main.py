"""
A common print resolution is 300 DPI, so for an 8.5 x 11-inch paper, the pixel dimensions would be 2550 x 3300 
pixels (8.5 inches * 300 DPI by 11 inches * 300 DPI).
"""

from PIL import Image, ImageDraw, ImageFont
import os
from myKwargs import MyKwargs


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
            "page_gutters": [300,100,100,100],
            "line_spacing": 20,
            "answer_spacing": 5,
            "label_spacing": 5,
            "zebra_shading": True,
            "label_style": None,
            "que_ident_style": None,
        }
        """
        print(kwargs)

        # "label_style": None,
        # "que_ident_style": None,

        self.dpi = kwargs.get("dpi", 288)
        self.page_size = kwargs.get("page_size", (8.5, 11))
        self.bubble_size = kwargs.get("bubble_size", 15)
        self.bubble_ratio = kwargs.get("bubble_ratio", 1)
        self.bubble_shape = kwargs.get("bubble_shape", "circle")

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
        self.page_gutters = kwargs.get("page_gutters", 5)

        self.zebra_shading = kwargs.get("zebra_shading", False)

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

        try:
            self.alignment_image = open_image(self.img_align_path)
            # Proceed with your operations on the image
        except FileNotFoundError as e:
            print(e)

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

    def addRectangle(self, x, y, w, h, color=(0, 0, 0), line=2):
        self.draw.rectangle([x, y, x + w, y + h], outline=color, width=line)

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

        x = start_x
        y = start_y - (self.bubble_height)

        i = 0
        n = 1

        for _ in range(self.num_questions * self.num_ans_options):
            if i % self.num_ans_options == 0:
                x = start_x
                y += self.bubble_height + self.line_spacing

                if n < 10:
                    l = "0" + str(n)
                else:
                    l = str(n)
                self.addBubbleLabel(x, y, f"{l}. ")
                n += 1
                x += 75

            x += 25
            self.addBubble(x, y)
            label = chr((i % self.num_ans_options) + 65)
            self.addBubbleLabel(x, y, label, (200, 200, 200))

            x += self.bubble_width + self.answer_spacing

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

        top = self.page_gutters[0]
        right = self.page_gutters[3]

        self.pasteAlignmentImages(positions)
        self.drawTestNumBoxes(500, 100, 60, 75, 8)
        self.drawSignatureLine(1350, 100)
        self.pasteImage(
            self.img_width // 2 - self.logo_image.width // 2, 50, self.logo_image
        )
        self.addAnswerBubbles(right, top)

    def saveImage(self, outname="temp.png", show=False):
        # Save the image
        print("saving...")
        # self.final_image = Image.alpha_composite(self.image, self.overlay)
        self.image.save("./generatedSheets/temp3.png")
        self.image.save("./generatedSheets/temp3.pdf")
        # self.image.show()


import sys


def usage():
    """
    Usage function for the custom scantron generator.

    Required Arguments:
        questions=int          Number of questions (25, 50, 100, 200; default=50).
        options=int            Number of lettered options per question (default=7).

    Optional Arguments:
        signature=bool         Include a signature line (default=True).
        test_id=bool           Include test ID boxes (default=True).
        info_location=str      Location for student info (top, left, right; default=top).
        border_size=float      Size of the checkerboard border in inches (.5 inches).
        check_size=float       Size of individual checks in the checkerboard in inches (default value recommended).
        logo_path=str          Path to an optional logo image file.
        header=str             Custom header text for the scantron.

    Example:
        python script.py questions=100 options=5 signature=False test_id=True info_location=left border_size=0.5 check_size=0.1 logo_path=/path/to/logo.png header="Exam 101"

    Note: Boolean values can be passed as True/False.
    """
    print(usage.__doc__)


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
        page_gutters         (list): pixel size of any additional padding for [top,right,bottom,left]
        line_spacing        (int): pixel padding between lines of answers
        answer_spacing      (int): pixel padding between answer bubbles
        label_spacing       (int): pixel padding between label and bubble
        zebra_shading       (bool): Shade behind alternating lines? True / False
        label_style         (str): Style string for the A B C .... (tbd)
        que_ident_style     (str): Style string for the 1. 2. 3. .... (tbd)
    """

    info = {
        "page_size": (8.5, 11),
        "img_align_path": "./assets/images/target_144x.png",
        "logo_path": "./assets/images/LiveTestLogo_144x.png",
        "num_ans_options": 4,
        "num_questions": 20,
        "dpi": 288,
        "font_size": 12,
        "bubble_shape": "circle",
        "bubble_size": 15,
        "bubble_ratio": 1,
        "font_path": "./assets/fonts/RobotoMono-Regular.ttf",
        "font_bold": "./assets/fonts/RobotoMono-Bold.ttf",
        "page_gutters": (300, 100, 100, 50),
        "line_spacing": 10,
        "answer_spacing": 5,
        "label_spacing": 5,
        "zebra_shading": True,
        "label_style": None,
        "que_ident_style": None,
        "font_alpha": 50,
    }

    pictron = Pictron(**info)
    pictron.generate()
    pictron.saveImage()
