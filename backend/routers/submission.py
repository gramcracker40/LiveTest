from fastapi import HTTPException, APIRouter
from pydantic import BaseModel
from tables import Submission, Student, Test
from db import session
from models.submission import CreateSubmission, GetSubmission, UpdateSubmission

router = APIRouter(
    prefix="/submission",
    tags=["submission"],
    responses={404: {"description": "Not found"}},
    redirect_slashes=True
)

@router.post("/")
def create_submission(submission: CreateSubmission):
    student = session.query(Student).get(submission.student_id)
    test = session.query(Test).get

    db_submission = Submission(**submission.__dict__)
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