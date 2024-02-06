import json
from rich import print
import shutil


with open("fontfind.out") as f:
    fonts = f.read().split("\n")


uniqueFonts = {}
for font in fonts:
    parts = font.split("/")
    key = parts[-1]
    if not key in uniqueFonts:
        uniqueFonts[key] = font
    print(parts[-1])


for key, path in uniqueFonts.items():
    print(key)
    # copy the contents of the demo.py file to  a new file called demo1.py
    shutil.copyfile(path, key.replace(" ", "_"))
