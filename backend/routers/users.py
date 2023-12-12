"""
# this file implements "/users" and all routes stemming from it

Handles all operations necessary for students and teachers in the API
CRUD routes 
Login route
"""
from fastapi import HTTPException, APIRouter, Depends
from sqlalchemy.exc import IntegrityError
from tables import Student, Teacher
from passlib.hash import pbkdf2_sha256
from typing import List
from jwt import jwt_token_verification
from models.users import (
    CreateStudent,
    CreateTeacher,
    GetStudent,
    GetTeacher,
    UpdateStudent,
    UpdateTeacher,
)
from db import session

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
    redirect_slashes=True,
)


# TEACHERS
@router.post("/teachers/", response_model=GetTeacher)#dependencies=[Depends(jwt_token_verification)])
def create_teacher(teacher: CreateTeacher):
    try:
        new_teacher = Teacher(name=teacher.name, email=teacher.email)
        new_teacher.password = pbkdf2_sha256.hash(teacher.password)
        session.add(new_teacher)
        session.commit()
    except IntegrityError as e:
        session.rollback()
        raise HTTPException(
            status_code=400, detail="Teacher with this email already exists"
        )

    return new_teacher


@router.get("/teachers/", response_model=List[GetTeacher])
def get_all_teachers():
    teachers = session.query(Teacher).all()
    return teachers


@router.get("/teachers/{teacher_id}", response_model=GetTeacher)
def get_teacher_by_id(teacher_id: int):
    teacher = session.query(Teacher).filter(Teacher.id == teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")

    return teacher


@router.patch("/teachers/{teacher_id}")
def update_teacher(teacher_id: int, update_data: UpdateTeacher):
    teacher = session.query(Teacher).filter(Teacher.id == teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")

    try:
        for key in update_data.model_dump():
            value = getattr(update_data, key)

            if key == "password" and value:
                value = pbkdf2_sha256.hash(value)

            if value:
                setattr(teacher, key, value)

        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=400, detail="Teacher with this email already exists"
        )

    return teacher


@router.delete("/teachers/{teacher_id}")
def delete_teacher(teacher_id: int):
    teacher = session.query(Teacher).filter(Teacher.id == teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")

    session.delete(teacher)
    session.commit()

    return {"message": "Teacher deleted successfully"}


# STUDENTS
@router.post("/students/", response_model=GetStudent)
def create_student(student: CreateStudent):
    try:
        new_student = Student(
            name=student.name, email=student.email, M_number=student.M_number
        )
        new_student.password = pbkdf2_sha256.hash(student.password)
        session.add(new_student)
        session.commit()
    except IntegrityError as e:
        session.rollback()
        err = str(e)

        if "students.email" in err:
            raise HTTPException(
                status_code=400, detail="Student with this email already exists"
            )
        elif "students.M_number" in err:
            raise HTTPException(
                status_code=400, detail="Student with this M_number already exists"
            )

    student = (
        session.query(Student).filter(Student.M_number == new_student.M_number).first()
    )
    return student


@router.get("/students/", response_model=List[GetStudent])
def get_all_students():
    students = session.query(Student).all()
    return students


@router.get("/students/{student_id}", response_model=GetStudent)
def get_student_by_id(student_id: int):
    student = session.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    return student


@router.patch("/students/{student_id}")
def update_student(student_id: int, update_data: UpdateStudent):
    student = session.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    try:
        for key in update_data.model_dump():
            value = getattr(update_data, key)

            if key == "password" and value:
                value = pbkdf2_sha256.hash(value)

            if value:
                setattr(student, key, value)

        session.commit()
    except IntegrityError as e:
        session.rollback()
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
def delete_student(student_id: int):
    student = session.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    session.delete(student)
    session.commit()

    return {"message": "Student deleted successfully"}
