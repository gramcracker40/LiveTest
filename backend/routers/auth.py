from tables import Student, Teacher
from passlib.hash import pbkdf2_sha256
from models.auth import Login
from db import session
from env import secret_key
from fastapi import Header, HTTPException, Security, APIRouter
from pydantic import ValidationError
from jose import jwt, JWTError, ExpiredSignatureError

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
            "email": found_user.email,
            "name": found_user.name,
            "id": found_user.id,
            "type": user_type,
        }
        access_token = jwt.encode(login_details, secret_key, algorithm="HS256")
        message = f"Successfully logged in {found_user.name}"

        return {
            "message": message, 
            "access_token": access_token,
            "email": found_user.email,
            "name": found_user.name,
            "id": found_user.id,
            "type": user_type,
        }
    else:
        return HTTPException(404, detail="User login info not valid")
    

def jwt_token_verification(access_token: str = Header()):
    try:
        # decode and verify the JWT using the application's secret key.
        # if it is successfully decoded, we allow the route to run.
        return jwt.decode(access_token, secret_key, algorithms=["HS256"])

    except ExpiredSignatureError:
        raise HTTPException(status_code=409, detail="The JWT submitted is expired. Please login again")

    except JWTError as e:
        raise HTTPException(status_code=401, detail="The JWT submitted is invalid")


def get_current_user(access_token: str = Header()):
    try:
        payload = jwt.decode(access_token, secret_key, algorithms=["HS256"])
        user_id = payload.get("id")
        user_type = payload.get("type")
        if user_id is None or user_type is None:
            raise HTTPException(status_code=403, detail="Invalid token")
        
        user = get_user_from_id(user_id, user_type)
        print(f"got user id! {user_id}")
        return user
    except (JWTError, ValidationError) as e:
        raise HTTPException(status_code=403, detail="Could not validate credentials")


def get_user_from_id(user_id: int, user_type: str):
    if user_type == "teacher":
        user = session.query(Teacher).filter(Teacher.id == user_id).first()
    elif user_type == "student":
        user = session.query(Student).filter(Student.id == user_id).first()
    else:
        raise HTTPException(status_code=404, detail="User type not recognized")
    
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user
