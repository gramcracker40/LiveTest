from pydantic import BaseModel, StringConstraints
from typing_extensions import Annotated
from fastapi import UploadFile, Form

class CreateSubmission(BaseModel):
    submission_image: UploadFile
    student_id: int = Form(...)
    test_id: str = Form(...)
    
class UpdateSubmission(BaseModel):
    answers: str
    grade: float
    student_id: int
    test_id: int

class GetSubmission(BaseModel):
    id: int
    student_id: int
    student_name: str 
    grade: float
    answers: str
    