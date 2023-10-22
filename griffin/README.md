Of course, Terry! I'll consolidate everything into a neat package for you. We'll create a class that allows for this sequence of operations to be performed on the scantron image:

1. Load the image.
2. Resize the image to the specified dimensions.
3. Rotate the image so it's orthogonal.
4. Crop it to only retain the region of interest.

Here's the consolidated set of functions:

```python
import cv2
import numpy as np

class ScantronProcessor:
    
    def __init__(self, image_path):
        self.image = cv2.imread(image_path)
    
    def resize(self, width, height):
        self.image = cv2.resize(self.image, (width, height))
    
    def rotate_to_orthogonal(self):
        # Convert image to grayscale
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        # Use the Hough transform to detect lines in the image.
        lines = cv2.HoughLinesP(gray, 1, np.pi / 180, 100, minLineLength=200, maxLineGap=5)
        angles = []
        for line in lines:
            x1, y1, x2, y2 = line[0]
            # Compute the angle of the line
            angle = np.arctan2(y2 - y1, x2 - x1) * 180. / np.pi
            angles.append(angle)
        # Take the median angle
        median_angle = np.median(angles)
        # Rotate the image by the negative median angle
        (h, w) = self.image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, median_angle, 1)
        self.image = cv2.warpAffine(self.image, M, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    
    def crop_to_roi(self, left_pct, right_pct):
        h, w, _ = self.image.shape
        left_bound = int(left_pct * w)
        right_bound = int(right_pct * w)
        self.image = self.image[:, left_bound:right_bound]
    
    def process(self, resize_dim=(1700, 4400), left_pct=0.15, right_pct=0.42):
        self.resize(*resize_dim)
        self.rotate_to_orthogonal()
        self.crop_to_roi(left_pct, right_pct)
        return self.image

    def save(self, output_path):
        cv2.imwrite(output_path, self.image)

# Example usage:
processor = ScantronProcessor("path_to_your_scantron.jpg")
processed_image = processor.process()
processor.save("path_to_output.jpg")
```

This class-based approach gives you the flexibility to apply the operations in any sequence you prefer. The `process` function provides a convenient way to apply all the operations at once with default parameters. You can modify those parameters as needed.