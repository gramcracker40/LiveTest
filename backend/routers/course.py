from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
from models.course import CreateCourse, UpdateCourse, GetCourse, ListCourses
from tables import Course, Student, Enrollment
from db import session
from jwt import jwt_token_verification

router = APIRouter(
    prefix="/course",
    tags=["course"],
    responses={404: {"description": "Not found"}},
    redirect_slashes=True,
)


@router.post("/")  # , dependencies=[Depends(jwt_token_verification)])
def create_course(course: CreateCourse):
    try:
        temp = Course(
            name=course.name,
            semester_season=course.semester_season,
            year=course.year,
            teacher_id=course.teacher_id,
            course_number=course.course_number,
        )
        session.add(temp)
        session.commit()
    except IntegrityError as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"Integrity error - {e}")

    return course


@router.get("/", response_model=List[GetCourse])
def get_all_courses():
    courses = session.query(Course).all()
    return courses if courses else {}


@router.get("/{course_id}", response_model=GetCourse)
def get_course_by_id(course_id: int):
    course = session.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    print(f"COURSE: {course}")
    return course


@router.put("/{course_id}")
def update_course(course_id: int, update_data: UpdateCourse):
    course = session.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    for key in update_data:
        setattr(course, key, update_data[key])

    session.commit()

    return course


@router.delete("/{course_id}")
def delete_course(course_id: int):
    course = session.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    session.delete(course)
    session.commit()

    return {"message": "Course deleted successfully"}
