from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
from models.course import CreateCourse, UpdateCourse, GetCourse, ListCourses
from tables import Course, Student, students_courses_association
from db import session
from jwt import jwt_token_verification

router = APIRouter(
    prefix="/course",
    tags=["course"],
    responses={404: {"description": "Not found"}},
)

@router.post("/") #, dependencies=[Depends(jwt_token_verification)])
def create_course(course: CreateCourse):
    try:
        temp = Course(name=course.name, semester_season=course.semester_season, 
                      year=course.year, teacher_id=course.teacher_id, 
                      course_number=course.course_number)
        session.add(temp)
        session.commit()
    except IntegrityError as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"Integrity error - {e}")

    return course

@router.get("/", response_model=List[GetCourse])
def get_all_courses():
    courses = session.query(Course).all()
    return courses

@router.get("/{course_id}", response_model=GetCourse)
def get_course_by_id(course_id: int):
    course = session.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
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


@router.post("/{course_id}/student/{student_id}")
def add_student_to_course(course_id:int, student_id:int):
    course = session.query(Course).filter(Course.id == course_id).first()
    student = session.query(Student).filter(Student.id == student_id).first()

    if not course:
        raise HTTPException(404, detail=f"course_id: {course_id} not found")
    elif not student:
        raise HTTPException(404, message=f"student_id: {student_id} not found")
    else:
        enrollment = students_courses_association(student_id=student.id, course_id=course.id)
        session.add(enrollment)
        session.commit()
        return {"message": f"Successfully added {student.name} into {course.name}"}
    
@router.delete("/{course_id}/student/{student_id}")
def remove_student_from_course(course_id:int, student_id:int):
    course = session.query(Course).filter(Course.id == course_id).first()
    student = session.query(Student).filter(Student.id == student_id).first()

    if not course:
        raise HTTPException(404, detail=f"course_id: {course_id} not found")
    elif not student:
        raise HTTPException(404, message=f"student_id: {student_id} not found")
    else:
        enrollment = session.query(students_courses_association)\
            .filter(students_courses_association.student_id == student.id, 
                    students_courses_association.course_id == course.id).first()
        
        if enrollment:
            session.delete(enrollment)
            session.commit()
            return {"message": f"Successfully removed {student.name} from {course.name}"}
        else:
            raise HTTPException(404, detail=f"{student.name} is not in {course.name}")

        
    