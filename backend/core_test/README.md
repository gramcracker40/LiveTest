# Originally intended core functionality of LiveTest

## Includes

Processing techniques for grading Scantron form 882Es

Started off trying to process these, figured why not just make custom answer sheets that fit our purpose later on. 

### Grading Scantron form 882Es

  Step 1: start off by running isolate_document.py on the image given. this function starts by finding a 5 vertex contour (Scantron form 882E). It then isolates the scantron and crops it completely using a bounding estimation technique, providing a consistent form for the Scantron to be evaluated in step 2.
  Step 2: Crop the scantron consistently to the answers after a four point transformation. 
    draw vertical partitions between A, B, C, D, E and then detect the shaded in regions for
    each answer
