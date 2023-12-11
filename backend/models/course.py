from typing import List
from pydantic import BaseModel
from models.users import GetStudent
from typing import Optional


class CreateCourse(BaseModel):
    name: str
    semester_season: str
    course_number: int
    year: int
    teacher_id: int


class UpdateCourse(BaseModel):
    name: Optional[str]
    semester_season: Optional[str]
    course_number: Optional[int]
    year: Optional[int]
    teacher_id: Optional[int]


class GetCourse(CreateCourse):
    id: int
    students: List[GetStudent]


class ListCourses(BaseModel):
    courses: List[GetCourse]
