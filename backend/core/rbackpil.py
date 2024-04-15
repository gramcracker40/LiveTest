#!/usr/local/bin/python3

from PIL import Image
from math import sqrt


def distance(c1, c2):
    """Distance between two rgb colors"""
    d = sqrt(
        pow((c2[0] - c1[0]), 2) + pow((c2[1] - c1[1]), 2) + pow((c2[2] - c1[2]), 2)
    )

    return d / sqrt(pow(255, 2) + pow(255, 2) + pow(255, 2))


def remove_background(**kwargs):
    """remove the background color of an image"""

    imgname = kwargs.get("imgname", None)
    dst = kwargs.get("dst", None)
    color = kwargs.get("color", None)
    threshold = kwargs.get("threshold", 0.2)

    if color == None:
        color, _ = determine_background(imgname)

    print(color)

    im = Image.open(imgname).convert("RGBA")

    w, h = im.size

    ccolor = (color[0], color[1], color[2], 0)

    for y in range(h):
        for x in range(w):
            p = im.getpixel((x, y))
            d = distance(color, p[0:3])
            if d < threshold:
                im.putpixel((x, y), ccolor)

    if dst != None:
        im.save(dst)
    else:
        im.show()


def determine_background(img):
    """Figure out the color of an images background"""
    if isinstance(img, str):
        img = Image.open(img).convert("RGBA")

    colors = {}

    for pixel in img.getdata():
        print(pixel)
        if not pixel in colors:
            colors[pixel] = 0
        colors[pixel] += 1

    print(colors)
    for key, value in sorted(
        colors.items(), key=lambda item: (item[1], item[0]), reverse=True
    ):
        return (key, value)

    return (225, 225, 225), 0


if __name__ == "__main__":

    filename = "/Users/griffin/Dropbox/Scripts-random/image_projects/ClosestColor/Full-Moon.jpg"
    dst = "/Users/griffin/Dropbox/Scripts-random/image_projects/ClosestColor/Full-Moon_out.png"
    filename = "/Users/griffin/Dropbox/Scripts-random/image_projects/image_processing/smiley.jpg"
    dst = "/Users/griffin/Dropbox/Scripts-random/image_projects/image_processing/smiley_back.png"
    filename = (
        "/Users/griffin/Dropbox/Scripts-random/image_projects/image_processing/cat.jpg"
    )
    dst = "/Users/griffin/Dropbox/Scripts-random/image_projects/image_processing/catout.png"
    filename = "/Users/griffin/Dropbox/Scripts-random/image_projects/AsciiStepbyStep/dwight.jpg"
    dst = "/Users/griffin/Dropbox/Scripts-random/image_projects/AsciiStepbyStep/dwight_out.png"
    filename = "/Users/griffin/Dropbox/Scripts-random/image_projects/DryRun/penguin.png"
    dst = "/Users/griffin/Dropbox/Scripts-random/image_projects/DryRun/penguin_out.png"

    # remove_background(imgname=filename,threshold=.1,dst=dst)
    remove_background(imgname=filename, threshold=0.1, dst=dst)
