from pydantic import BaseModel, StringConstraints
from typing_extensions import Annotated

class CreateSubmission(BaseModel):
    submission_photo: str
    file_extension: Annotated[str, StringConstraints(pattern=r'^(jpg|png)$')]
    student_id: int
    test_id: str
    
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
    