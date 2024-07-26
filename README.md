# LiveTest - open-source, server-based, OMR testing software. 

  Create your school's custom answer sheets and grade them in the browser!

  free, easy, consistent process for server based dynamic OMR grading/scanning using highly customizable answer sheets that can be integrated with any school. 

![Courses Page](frontend\app\dist\assets\CoursesPage.png)

![Course Page](frontend\app\dist\assets\CoursePage.png)

![Student Enrollment Page](frontend\app\dist\assets\StudentEnrollment.png)

![Teacher Course List Page](frontend\app\dist\assets\TeacherCourseList.png)

![Create Course Page](frontend\app\dist\assets\CreateCoursePage.png)

![Create Test Page](frontend\app\dist\assets\CreateTestPage.png)

![LIVE Test Page](frontend\app\dist\assets\LIVETestPage.png)

![SubmissionPage](frontend\app\dist\assets\SubmissionPage.png)

<img src="frontend/app/src/assets/LiveTestLogo.png" alt="LiveTestLogo" width="700" height="900">

# /backend
### /answer_sheets  - research
  - main.py --> customizable, dynamically gradable test answer sheets
  - grader.py --> dynamic OMRGrader module that grades answer_sheets produced by main.py

### app.py   
  - builds and orchestrates the backend fastapi/sqlalchemy application
        
        
# /frontend 
  implements the demo app built using Vite React JavaScript to showcase the abilities of the backend. 


### Docker production
  docker-compose
