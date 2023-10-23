To obtain an accurate statistical depiction of a scantron in CSV format


  Roadmap
############################################################################
  ## Normalize the image. cropping scantron answers after resize. 

find edges on scantron and crop to consistent photo for opencv to go off of. 
normalize the size of the scantron to be consistently the same
use contours. 

flip the orientation to be exact on each side before running the model. 

### Resources:

edge detection using opencv and python --> https://www.youtube.com/watch?v=6cXV8dhNu50 

countour detection with cv2-python --> https://www.youtube.com/watch?v=IBQYqwq_w14 

cropping/ flipping orientation --> https://realpython.com/image-processing-with-the-python-pillow-library/ 

############################################################################

## Optical Mark Recognition (OMR) - identifying the marked in circle for each row

is the process of automatically analyzing human-marked documents and interpreting their results. done with opencv


### Resources 

https://pyimagesearch.com/2016/10/03/bubble-sheet-multiple-choice-scanner-and-test-grader-using-omr-python-and-opencv/


############################################################################