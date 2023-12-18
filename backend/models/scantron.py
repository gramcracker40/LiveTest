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


class GetScantron(UpdateScantron):
    id: int
    graded_image: str
