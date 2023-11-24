from typing import List
from pydantic import BaseModel
from models.users import GetStudent

class CreateCourse(BaseModel):
    name: str
    semester_season: str
    course_number: int
    year: int
    teacher_id: int

class UpdateCourse(CreateCourse):
    pass

class GetCourse(CreateCourse):
    id: int
    students: List[GetStudent]

class ListCourses(BaseModel):
    courses: List[GetCourse]
