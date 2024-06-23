# LiveTest - open-source, server-based, OMR testing software. 

  Create your school's custom answer sheets and grade them in the browser!



  free, easy, consistent process for server based dynamic OMR grading/scanning using highly customizable answer sheets that can be integrated with any school easily. 



<img src="frontend/app/src/assets/LiveTestLogo.png" alt="LiveTestLogo" width="700" height="900">

# /backend
### /answer_sheets  - research
  - main.py --> customizable, dynamically gradable test answer sheets
  - grader.py --> dynamic OMRGrader module that grades answer_sheets produced by main.py

### app.py   
  - builds and orchestrates the backend fastapi/sqlalchemy application
        
        
# /frontend 
  demo app built using Vite React JavaScript to showcase the abilities of the backend. 

### Docker development
  docker build -f backend/deploy/Dockerfile -t livetest_api .
  docker run -p 8000:8000 livetest_api

  docker build -f frontend/deploy/Dockerfile -t livetest .
  docker run livetest

### Docker production
  docker-compose 