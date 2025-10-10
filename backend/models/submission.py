from pydantic import BaseModel, StringConstraints, Field
from typing_extensions import Annotated, Optional, Dict
from fastapi import UploadFile, Form
from datetime import datetime

class CreateSubmission(BaseModel):
    submission_image: UploadFile
    student_id: Optional[int] = Form(None) 
    test_id: str = Form(...)

class UpdateSubmission(BaseModel):
    answers: str
    grade: float
    student_id: int
    test_id: int

class GetSubmission(BaseModel):
    id: int
    student_id: Optional[int] = None
    student_name: str
    grade: float
    submission_time: Optional[datetime] = None

class GetStudentSubmission(BaseModel):
    id: int
    student_id: Optional[int] = None
    grade: float
    
class AnswerDetail(BaseModel):
    choice: str = Field(..., example="A")
    correct: bool = Field(..., example=True)

class GetSubmissionAnswers(BaseModel):
    answers: Dict[int, AnswerDetail] = Field(..., example={"1": {"choice": "A", "correct": True}})
