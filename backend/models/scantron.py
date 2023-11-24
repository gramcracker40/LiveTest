from pydantic import BaseModel

class CreateScantron(BaseModel):
    scantron_photo: bytes
    student_id: int
    test_id: int
    
class UpdateScantron(BaseModel):
    answers: str
    grade: float
    student_id: int
    test_id: int

class GetScantron(BaseModel):
    id: int
    graded_image: str
    answers: str
    grade: float
    student_id: int
    test_id: int