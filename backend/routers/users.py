from fastapi import FastAPI, HTTPException, Query, APIRouter, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from Models import Scantron, Student, Teacher
from Database import session
from passlib.hash import pbkdf2_sha256

salty_value = "uvhbduogbosygbdfbgifad"

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

class Login(BaseModel): 
    email: str
    password: str

class CreateTeacher(BaseModel):
    name: str 
    email: str
    password: str

class CreateStudent(CreateTeacher):
    M_number: str
    


@router.post("/login/")
def login(login_info: Login):
    email = login_info['email']
    password = pbkdf2_sha256.hash(login_info['password'], secret=salty_value)

    teacher = Teacher.query.filter(Teacher.email == email, # and 
             Teacher.password == password)

    student = Student.query.filter(Student.email == email,
             Student.password == password)
    
    if teacher and not student:
        pass
    elif student and not teacher:
        pass
    else:
        HTTPException(404, detail="User login info not found")


@router.post("/teacher/")
def create_teacher(teacher: CreateTeacher):
    teacher = Teacher(**teacher.__dict__)
    session.add(teacher)
    session.commit()
    
    return teacher

@router.post("/student/")
def create_student(student: CreateStudent):
    student = Student(**student.__dict__)
    session.add(student)
    session.commit()
    
    return student
