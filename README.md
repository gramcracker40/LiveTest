# LiveTest ![LiveTest Logo](frontend/app/src/assets/LiveTestLogo.png)
<img src="frontend/app/src/assets/LiveTestLogo.png" alt="Alt text" width="50" height="50">
Mission statement: Provide a free, easy, consistent process for server based dynamic OMR grading/scanning using highly customizable answer sheets that can be integrated with any school easily. 

# /backend 
  python app built using 
    fastapi/    ASGI server
    sqlalchemy/ SQL Database
    opencv2/    Image Processing for OMRGrader module found in backend/answer_sheets/grader.py
    pillow/     Building the custom answer_sheets compatible with the LiveTest OMRGrader
