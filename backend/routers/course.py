# routers/course.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List

from models.course import CreateCourse, UpdateCourse, GetCourse, GetCourseMinimum
from models.users import GetStudentMinimum
from tables import Course, Student, Teacher
from db import get_db
# from routers.auth import jwt_token_verification

router = APIRouter(
    prefix="/course",
    tags=["course"],
    responses={404: {"description": "Not found"}},
    redirect_slashes=True,
)

@router.post("/")
def create_course(course: CreateCourse, db: Session = Depends(get_db)):
    try:
        temp = Course(**course.model_dump())
        db.add(temp)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="This course already exists")
    return course

@router.get("/", response_model=List[GetCourse])
def get_all_courses(db: Session = Depends(get_db)):
    return db.query(Course).all()

@router.get("/student/{student_id}", response_model=List[GetCourse])
def get_all_courses_for_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).get(student_id)
    if not student:
        raise HTTPException(404, detail=f"student_id: {student_id} not found")
    return student.courses

@router.get("/teacher/{teacher_id}", response_model=List[GetCourse])
def get_all_courses_for_teacher(teacher_id: int, db: Session = Depends(get_db)):
    teacher = db.query(Teacher).get(teacher_id)
    if not teacher:
        raise HTTPException(404, detail=f"teacher_id: {teacher_id} not found")
    return teacher.courses

@router.get("/{course_id}", response_model=GetCourse)
def get_course_by_id(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@router.get("/students/{course_id}", response_model=List[GetStudentMinimum])
def get_students_for_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).get(course_id)
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return course.students

@router.patch("/{course_id}")
def update_course(course_id: int, update_data: UpdateCourse, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    for key, value in update_data.model_dump().items():
        if value is not None:
            setattr(course, key, value)
    try:
        db.commit()
    except IntegrityError as err:
        db.rollback()
        if "UNIQUE" in str(err):
            raise HTTPException(status_code=400, detail="A course with the same section, course number, name, season and year already exists.")
    return course

@router.delete("/{course_id}")
def delete_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    db.delete(course)
    db.commit()
    return {"message": "Course deleted successfully"}
