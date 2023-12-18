from fastapi import HTTPException, APIRouter, Depends
from tables import Student, Teacher
from passlib.hash import pbkdf2_sha256
from jose import jwt
from jwt import jwt_token_verification
from models.auth import Login
from db import session
from env import secret_key

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
    redirect_slashes=True,
)


@router.post("/login")
async def login(login_info: Login):
    """
    Login as a teacher or student with username/password
    """
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
    authenticated = (
        pbkdf2_sha256.verify(login_info.password, found_user.password)
        if found_user
        else False
    )

    # return the outcome of the authentication check
    if authenticated:
        login_details = {
            "name": found_user.name,
            "id": found_user.id,
            "type": user_type,
        }
        access_token = jwt.encode(login_details, secret_key, algorithm="HS256")
        message = f"Successfully logged in {found_user.name}"

        return {"message": message, "access_token": access_token}
    else:
        return HTTPException(404, detail="User login info not valid")
