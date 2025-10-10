# routers/enrollment.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
from tables import Course, Student, Enrollment
from db import get_db
from routers.auth import jwt_token_verification

router = APIRouter(
    prefix="/enrollment",
    tags=["enrollment"],
    responses={404: {"description": "Not found"}},
    redirect_slashes=True,
)


@router.post("/{course_id}/student/{student_id}")
def add_student_to_course(course_id: int, student_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    student = db.query(Student).filter(Student.id == student_id).first()

    try:
        if not course:
            raise HTTPException(404, detail=f"course_id: {course_id} not found")
        elif not student:
            raise HTTPException(404, detail=f"student_id: {student_id} not found")
        else:
            enrollment = Enrollment(student_id=student.id, course_id=course.id)
            db.add(enrollment)
            db.commit()
            return {"message": f"Successfully added {student.name} into {course.name}"}
    except IntegrityError:
        db.rollback()
        raise HTTPException(400, detail=f"{student.name} is already in {course.name}")


@router.delete("/{course_id}/student/{student_id}")
def remove_student_from_course(course_id: int, student_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    student = db.query(Student).filter(Student.id == student_id).first()

    if not course:
        raise HTTPException(404, detail=f"course_id: {course_id} not found")
    elif not student:
        raise HTTPException(404, detail=f"student_id: {student_id} not found")
    else:
        enrollment = (
            db.query(Enrollment)
            .filter(
                Enrollment.student_id == student.id, Enrollment.course_id == course.id
            )
            .first()
        )

        if enrollment:
            db.delete(enrollment)
            db.commit()
            return {
                "message": f"Successfully removed {student.name} from {course.name}"
            }
        else:
            raise HTTPException(404, detail=f"{student.name} is not in {course.name}")
