# routers/users.py
"""
# this file implements "/users" and all routes stemming from it

Handles all operations necessary for students and teachers in the API
CRUD routes 
Login route
"""
from fastapi import HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from tables import Student, Teacher
from passlib.hash import pbkdf2_sha256
from typing import List
from routers.auth import jwt_token_verification
from models.users import (
    CreateStudent,
    CreateTeacher,
    GetStudent,
    GetTeacher,
    UpdateStudent,
    UpdateTeacher,
)
from db import get_db

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
    redirect_slashes=True,
)


# TEACHERS
@router.post("/teachers/")  # dependencies=[Depends(jwt_token_verification)])
def create_teacher(teacher: CreateTeacher, db: Session = Depends(get_db)):
    try:
        new_teacher = Teacher(name=teacher.name, email=teacher.email)
        new_teacher.password = pbkdf2_sha256.hash(teacher.password)
        db.add(new_teacher)
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=400, detail="Teacher with this email already exists"
        )

    return {}


@router.get("/teachers/", response_model=List[GetTeacher])
def get_all_teachers(db: Session = Depends(get_db)):
    teachers = db.query(Teacher).all()
    return teachers


@router.get("/teachers/{teacher_id}", response_model=GetTeacher)
def get_teacher_by_id(teacher_id: int, db: Session = Depends(get_db)):
    teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")

    return teacher


@router.patch("/teachers/{teacher_id}")
def update_teacher(teacher_id: int, update_data: UpdateTeacher, db: Session = Depends(get_db)):
    teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")

    try:
        for key in update_data.model_dump():
            value = getattr(update_data, key)

            if key == "password" and value:
                value = pbkdf2_sha256.hash(value)

            if value:
                setattr(teacher, key, value)

        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, detail="Teacher with this email already exists"
        )

    return teacher


@router.delete("/teachers/{teacher_id}")
def delete_teacher(teacher_id: int, db: Session = Depends(get_db)):
    teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")

    db.delete(teacher)
    db.commit()

    return {"message": "Teacher deleted successfully"}


# STUDENTS
@router.post("/students/")
def create_student(student: CreateStudent, db: Session = Depends(get_db)):
    try:
        new_student = Student(
            name=student.name, email=student.email
        )
        new_student.password = pbkdf2_sha256.hash(student.password)
        db.add(new_student)
        db.commit()
    except IntegrityError as e:
        db.rollback()
        err = str(e)

        if "students.email" in err:
            raise HTTPException(
                status_code=400, detail="Student with this email already exists"
            )
        elif "students.M_number" in err:
            raise HTTPException(
                status_code=400, detail="Student with this M_number already exists"
            )

    return {}


@router.get("/students/", response_model=List[GetStudent])
def get_all_students(db: Session = Depends(get_db)):
    students = db.query(Student).all()
    return students


@router.get("/students/{student_id}", response_model=GetStudent)
def get_student_by_id(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    return student


@router.patch("/students/{student_id}")
def update_student(student_id: int, update_data: UpdateStudent, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    try:
        for key in update_data.model_dump():
            value = getattr(update_data, key)

            if key == "password" and value:
                value = pbkdf2_sha256.hash(value)

            if value:
                setattr(student, key, value)

        db.commit()
    except IntegrityError as e:
        db.rollback()
        err = str(e)

        if "students.email" in err:
            raise HTTPException(
                status_code=400, detail="Student with this email already exists"
            )
        elif "students.M_number" in err:
            raise HTTPException(
                status_code=400, detail="Student with this M_number already exists"
            )

    return student


@router.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    db.delete(student)
    db.commit()

    return {"message": "Student deleted successfully"}
