import json
import base64
import io
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, APIRouter, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List
import cv2
from tables import Submission, Student, Test
from db import session
from models.submission import CreateSubmission, GetSubmission, UpdateSubmission
from answer_sheets.grader import OMRGrader
from routers.auth import get_current_user

router = APIRouter(
    prefix="/submission",
    tags=["submission"],
    responses={404: {"description": "Not found"}},
    redirect_slashes=True
)


@router.post("/")
def create_submission_live(submission: CreateSubmission, user=Depends(get_current_user)):
    '''
    # TODO add a check to make sure the given student is actually in the course associated with the test
    # TODO make sure the student has not already submitted to the test
    # TODO add a check to make sure that the test is actually "Live"

    create a submission using the offical LiveTest answer sheets.

    the Test being submitted to must be "Live". i.e the time must be in between
    the set start and end datetimes. 
    '''
    test = session.query(Test).get(submission.test_id)
    test_key = json.loads(test.answers)

    print(f"{test.name} Key: {test_key}")

    if not test:
        raise HTTPException(404, detail="test was not found. please refresh")

    grader = OMRGrader(
        num_choices=test.num_choices, 
        num_questions=test.num_questions
    )
    grade, graded, choices = grader.run(bytes_obj=submission.submission_image, key=test_key)

    print(f"grade: {grade}\ngraded: {graded}\nchoices: {len(choices)}")

    new_submission = Submission(
        submission_image=submission.submission_image,
        graded_image=grader.image.__bytes__, 
        answers=json.dumps({
            question_num: (choices[question_num][2], graded[question_num])
            for question_num in graded
        }), # {1: ("A", True), 2: ("F", False)}  -->  answers (JSON str)
        grade=grade,
        student_id=user.id,
        test_id=test.id
    )

    print(f"NEW SUBMISSION: {new_submission}")

    session.add(new_submission)
    session.commit()


    



@router.delete("/{submission_id}")
def delete_submission(submission_id: int):
    submission = session.query(Submission).get(submission_id)
    if submission is None:
        raise HTTPException(status_code=404, detail="Submission not found")
    
    session.delete(submission)
    session.commit()

    return {"detail": "successfully deleted submission"}


@router.get("/{submission_id}", response_model=GetSubmission)
def get_submission(submission_id: int):
    submission = session.query(Submission).get(submission_id)
    
    if submission is None:
        raise HTTPException(status_code=404, detail="Submission not found")
    return submission


@router.get("/test/{test_id}", response_model=List[GetSubmission])
def get_submissions_for_test(test_id: str):
    test = session.query(Test).get(test_id)

    if test is None:
        raise HTTPException(status_code=404, detail="Test not found")
    
    return test.submissions


@router.get("/image/{submission_id}")
def get_submission_image(submission_id: int):
    submission = session.query(Submission).get(submission_id)

    if not submission:
        raise HTTPException(status_code=404, detail="Test not found")
    
    return StreamingResponse(io.BytesIO(submission.graded_photo), media_type="image/jpg")


@router.get("/student/{student_id}", response_model=List[GetSubmission])
def get_submissions_for_student(student_id: int):
    student = session.query(Student).get(student_id)

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    return student.submissions





# @router.post("/882E")
# def create_submission_882E(submission: CreateSubmission):
#     '''
#     Create a submission using a Form 882E
#     '''
#     # query student and test, ensure request validity
#     student = session.query(Student).get(submission.student_id)
#     test = session.query(Test).get(submission.test_id)

#     if not student:
#         raise HTTPException(404, detail=f"student {submission.student_id} does not exist")
#     if not test:
#         raise HTTPException(404, detail=f"test {submission.test_id} does not exist")

#     try: 
#         # turn base64 string into bytes obj
#         submission_image = base64.b64decode(submission.submission_photo.encode("utf-8"))
#         test_key = json.loads(test.answers)
#         test_key = {int(x): test_key[x] for x in test_key}
#         print("test_key", json.dumps(test_key))
#         # create ScantronProcessor for handling submission 
#         # new_submission = ScantronProcessor(
#         #     test_key, 
#         #     image=submission_image 
#         # )
#         # process the submission, obtaining user answers and grade
#         # graded_answers, grade = new_submission.process()
#         # # convert Matlike obj to bytes obj for storage in db
#         # image_buffer = cv2.imencode('.jpg', new_submission.image)[1]
#         # graded_image = image_buffer.tobytes()

#         # instantiate new submission obj
#         db_submission = Submission(
#             # graded_photo=graded_image, 
#             file_extension='jpg', 
#             num_questions=test.num_questions, 
#             # answers=json.dumps(graded_answers), 
#             # grade=grade, 
#             student_id=student.id, 
#             test_id=test.id
#         )
#         session.add(db_submission)
#         session.commit()
        
#         return {"detail": f"successfully submitted the answer key for {test.name}"}
#     except IntegrityError:
#         raise HTTPException(400, detail="Student has already submitted to this test")
#     except cv2.error as e:
#         print(str(e))
#         print("CV2 Error!!!")
#         session.rollback()
#         raise HTTPException(400, detail="Submission could not be processed, please try again.")
