from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
from models.course import CreateCourse, UpdateCourse, GetCourse, ListCourses
from tables import Course
from db import get_db
from jwt import jwt_token_verification

router = APIRouter(
    prefix="/course",
    tags=["course"],
    responses={404: {"description": "Not found"}},
)

@router.post("/") #, dependencies=[Depends(jwt_token_verification)])
def create_course(course: CreateCourse, db: Session = Depends(get_db)):
    try:
        temp = Course(name=course.name, semester_season=course.semester_season, 
                      year=course.year, teacher_id=course.teacher_id)
        db.add(temp)
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Course with this ID already exists")

    return course

@router.get("/", response_model=List[GetCourse])
def get_all_courses(db: Session = Depends(get_db)):
    courses = db.query(Course).all()
    return courses

@router.get("/{course_id}", response_model=GetCourse)
def get_course_by_id(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    return course

@router.put("/{course_id}")
def update_course(course_id: int, update_data: UpdateCourse, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    course.name = update_data.name
    course.course_number = update_data.course_number
    course.semester_season = update_data.semester_season
    course.year = update_data.year
    
    db.commit()
    
    return course

@router.delete("/{course_id}")
def delete_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    db.delete(course)
    db.commit()
    
    return {"message": "Course deleted successfully"}
