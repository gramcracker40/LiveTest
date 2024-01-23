from typing import List
from pydantic import BaseModel
from models.users import GetStudentMinimum
from models.test import GetTestMinimum
from typing import Optional


class CreateCourse(BaseModel):
    name: str
    semester_season: str
    course_number: int
    section: int
    year: int
    teacher_id: Optional[int]
    subject: str


class UpdateCourse(BaseModel):
    name: Optional[str] = None
    semester_season: Optional[str] = None
    course_number: Optional[int] = None
    section: Optional[int] = None
    year: Optional[int] = None
    teacher_id: Optional[int] = None
    subject: Optional[str] = None

class GetCourse(CreateCourse):
    id: int
    students: List[GetStudentMinimum]
    tests: List[GetTestMinimum]


class GetCourseMinimum(BaseModel):
    id: int
    name: str


class ListCourses(BaseModel):
    courses: List[GetCourse]
