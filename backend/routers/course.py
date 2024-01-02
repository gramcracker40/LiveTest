from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from typing import List
from models.course import CreateCourse, UpdateCourse, GetCourse, GetCourseMinimum
from tables import Course, Student, Teacher
from db import session
from jwt import jwt_token_verification

router = APIRouter(
    prefix="/course",
    tags=["course"],
    responses={404: {"description": "Not found"}},
    redirect_slashes=True,
)

@router.post("/")  # , #dependencies=[Depends(jwt_token_verification)])
def create_course(course: CreateCourse):
    try:
        temp = Course(**course.model_dump())
        session.add(temp)
        session.commit()
    except IntegrityError as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"This course already exists")

    return course


@router.get("/", response_model=List[GetCourse])
def get_all_courses():
    return session.query(Course).all()

@router.get("/student/{student_id}", response_model=List[GetCourseMinimum])
def get_all_courses_for_student(student_id: int):
    student = session.query(Student).get(student_id)

    if not student:
        raise HTTPException(404, detail=f"student_id: {student_id} not found")

    return [{"id": course.id, "name": course.name} 
                for course in student.courses]


@router.get("/teacher/{teacher_id}", response_model=List[GetCourseMinimum])
def get_all_courses_for_teacher(teacher_id: int):
    teacher = session.query(Teacher).get(teacher_id)

    if not teacher:
        raise HTTPException(404, detail=f"teacher_id: {teacher_id} not found")

    return [{"id": course.id, "name": course.name} 
                for course in teacher.courses]


@router.get("/{course_id}", response_model=GetCourse)
def get_course_by_id(course_id: int):
    course = session.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@router.patch("/{course_id}")
def update_course(course_id: int, update_data: UpdateCourse):
    course = session.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    for key, value in update_data.model_dump().items():
        if value != None:
            setattr(course, key, value)
    try:
        session.commit()
    except IntegrityError as err:
        session.rollback()
        if "UNIQUE" in str(err):
            raise HTTPException(status_code=400, detail="A course with the same section, course number, name, season and year already exists.")
    
    return course


@router.delete("/{course_id}")
def delete_course(course_id: int):
    course = session.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    session.delete(course)
    session.commit()

    return {"message": "Course deleted successfully"}
