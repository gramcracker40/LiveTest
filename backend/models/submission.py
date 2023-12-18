from pydantic import BaseModel

class CreateSubmission(BaseModel):
    submission_photo: str
    student_id: int
    test_id: str
    
class UpdateSubmission(BaseModel):
    answers: str
    grade: float
    student_id: int
    test_id: int

class GetSubmission(UpdateSubmission):
    id: int
    graded_image: str