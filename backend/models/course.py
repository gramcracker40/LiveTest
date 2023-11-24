from typing import List
from pydantic import BaseModel

class CreateCourse(BaseModel):
    name: str
    semester_season: str
    year: int
    teacher_id: int

class UpdateCourse(BaseModel):
    name: str
    semester_season: str
    year: int
    teacher_id: int

class GetCourse(BaseModel):
    id: int
    name: str
    semester_season: str
    year: int
    teacher_id: int

class ListCourses(BaseModel):
    courses: List[GetCourse]
