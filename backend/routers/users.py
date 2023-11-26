'''
# this file implements "/users" and all routes stemming from it

Handles all operations necessary for students and teachers in the API
CRUD routes 
Login route
'''
from fastapi import HTTPException, APIRouter, Depends
from sqlalchemy.exc import IntegrityError
from tables import Student, Teacher
from passlib.hash import pbkdf2_sha256
from typing import List
from jose import jwt
from jwt import jwt_token_verification
from models.users import Login, CreateStudent, CreateTeacher, \
        GetStudent, GetTeacher, UpdateStudent, UpdateTeacher
from db import session
from env import secret_key

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

@router.post("/login")
async def login(login_info: Login):
    # search for the potential teacher or student in the database. 
    teacher = session.query(Teacher).filter(Teacher.email == login_info.email).first()
    student = session.query(Student).filter(Student.email == login_info.email).first()
    
    # confirm the found teacher or student
    if teacher:
        found_user = teacher 
        user_type = "teacher"
    elif student:
        found_user = student
        user_type = "student"
    else:
        found_user = None
    
    # verify the password received against the one in DB for corresponding teacher/student. 
    authenticated = pbkdf2_sha256.verify(login_info.password, found_user.password) \
        if found_user else False

    # return the outcome of the authentication check
    if authenticated: 
        login_details = {
            "name": found_user.name, 
            "id": found_user.id, 
            "type": user_type
        }
        access_token = jwt.encode(login_details, secret_key, algorithm="HS256")
        message = f"Successfully logged in {found_user.name}"

        return {"message": message, "access_token": access_token}
    else:
        return HTTPException(404, detail="User login info not valid")

# TEACHERS
@router.post("/teacher", dependencies=[Depends(jwt_token_verification)])
def create_teacher(teacher: CreateTeacher):
    try:
        temp = Teacher(name=teacher.name, email=teacher.email)
        temp.password = pbkdf2_sha256.hash(teacher.password)
        session.add(temp)
        session.commit()
    except IntegrityError as e:
        session.rollback()
        raise HTTPException(status_code=400, detail="Teacher with this email already exists")

    return teacher

@router.get("/teachers/", response_model=List[GetTeacher])
def get_all_teachers():
    teachers = session.query(Teacher).all()
    return teachers

@router.get("/teacher/{teacher_id}", response_model=GetTeacher)
def get_teacher_by_id(teacher_id: int):
    teacher = session.query(Teacher).filter(Teacher.id == teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    return teacher

@router.put("/teacher/{teacher_id}")
def update_teacher(teacher_id: int, update_data: UpdateTeacher):
    teacher = session.query(Teacher).filter(Teacher.id == teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")

    teacher.email = update_data.email
    teacher.password = update_data.password
    
    session.commit()
    
    return teacher

@router.delete("/teacher/{teacher_id}")
def delete_teacher(teacher_id: int):
    teacher = session.query(Teacher).filter(Teacher.id == teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    session.delete(teacher)
    session.commit()
    
    return {"message": "Teacher deleted successfully"}

# STUDENTS
@router.post("/student")
def create_student(student: CreateStudent):
    try:
        temp = Student(name=student.name, email=student.email, M_number=student.M_number)
        temp.password = pbkdf2_sha256.hash(student.password)
        session.add(temp)
        session.commit()
    except IntegrityError as e:
        session.rollback()
        err = str(e)
        
        if "email" in err:
            raise HTTPException(status_code=400, detail="Student with this email already exists")
        elif "M_number" in err:
            raise HTTPException(status_code=400, detail="Student with this M_number already exists")

    return student

@router.get("/students/", response_model=List[GetStudent])
def get_all_students():
    students = session.query(Student).all()
    return students

@router.get("/student/{student_id}", response_model=GetStudent)
def get_student_by_id(student_id: int):
    student = session.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    return student

@router.put("/student/{student_id}")
def update_student(student_id: int, update_data: UpdateStudent):
    student = session.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    student.email = update_data.email
    student.password = update_data.password
    
    session.commit()
    
    return student


@router.delete("/student/{student_id}")
def delete_student(student_id: int):
    student = session.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    session.delete(student)
    session.commit()
    
    return {"message": "Student deleted successfully"}
