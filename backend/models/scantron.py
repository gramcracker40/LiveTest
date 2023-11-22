from pydantic import BaseModel

class ScantronCreate(BaseModel):
    scantron_photo: bytes
    student_id: int
    test_id: int
    
class Scantron(BaseModel):
    num_questions: int
    answers: str
    grade: float
    student_id: int
    test_id: int