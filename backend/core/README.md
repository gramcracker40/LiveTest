# Core functionality of LiveTest

## Includes

Process for grading Scantron form 882Es

Process for grading LiveTest purpose built answer sheets


### Grading Scantron form 882Es

  Step 1: start off by running isolate_document.py on the image given. this function starts by finding a 5 vertex contour (Scantron form 882E). It then isolates the scantron and crops it completely using a bounding estimation technique, providing a consistent form for the Scantron to be evaluated in step 2.

  
Lit review - find all similar research - take notes of everything