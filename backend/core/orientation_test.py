from ScantronProcessor import find_and_rotate, show_image
import os

test_dir = "../../test_data/OrientationTest"

file_paths = [os.path.join(root, filename) 
    for root, directories, files in os.walk(test_dir)
    for filename in files]

for path in file_paths:
    image = find_and_rotate(path)
    show_image(path, image)
