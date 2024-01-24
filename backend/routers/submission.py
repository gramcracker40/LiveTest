import json
import base64
from fastapi import HTTPException, APIRouter
from pydantic import BaseModel
import cv2
from tables import Submission, Student, Test
from db import session
from models.submission import CreateSubmission, GetSubmission, UpdateSubmission
from core.ScantronProcessor import ScantronProcessor

router = APIRouter(
    prefix="/submission",
    tags=["submission"],
    responses={404: {"description": "Not found"}},
    redirect_slashes=True
)

@router.post("/")
def create_submission(submission: CreateSubmission):
    # query student and test, ensure request validity
    student = session.query(Student).get(submission.student_id).first()
    test = session.query(Test).get(submission.test_id).first()

    if not student:
        raise HTTPException(404, detail=f"student {submission.student_id} does not exist")

    if not test:
        raise HTTPException(404, detail=f"test {submission.test_id} does not exist")

    # turn base64 string into bytes obj
    submission_image = base64.b64decode(submission.submission_photo.encode("utf-8"))
    
    # create ScantronProcessor for handling submission 
    new_submission = ScantronProcessor(
        json.loads(test.answers), 
        image=submission_image 
    )
    # process the submission, obtaining user answers and grade
    graded_answers, grade = new_submission.process()
    # convert Matlike obj to bytes obj for storage in db
    image_buffer = cv2.imencode('.jpg', new_submission.image)[1]
    graded_image = image_buffer.tobytes()

    # instantiate new submission obj
    db_submission = Submission(
        graded_photo=graded_image, 
        file_extension='.jpg', 
        num_questions=test.num_questions, 
        answers=json.dumps(graded_answers), 
        grade=grade, 
        student_id=student.id, 
        test=test.id
    )
    session.add(db_submission)
    session.commit()
    
    return {"detail": "successfully submitted the answer key for "}

@router.get("/{submission_id}", response_model=GetSubmission)
def read_submission(submission_id: int):
    db = session()
    db_Submission = db.query(Submission).filter(Submission.id == submission_id).first()
    db.close()
    if db_Submission is None:
        raise HTTPException(status_code=404, detail="Submission not found")
    return db_Submission

@router.put("/{submission_id}", response_model=UpdateSubmission)
def update_submission(submission_id: int, submission: CreateSubmission):
    db = session()
    db_submission = db.query(Submission).filter(Submission.id == submission).first()
    if db_submission is None:
        db.close()
        raise HTTPException(status_code=404, detail="Submission not found")
    for key, value in submission.model_dump().items():
        setattr(db_submission, key, value)
    db.commit()
    db.refresh(db_submission)
    db.close()
    return db_submission

@router.delete("/{Submission_id}", response_model=GetSubmission)
def delete_submission(Submission_id: int):
    db = session()
    db_Submission = db.query(Submission).filter(Submission.id == Submission_id).first()
    if db_Submission is None:
        db.close()
        raise HTTPException(status_code=404, detail="Submission not found")
    db.delete(db_Submission)
    db.commit()
    db.close()
    return db_Submission