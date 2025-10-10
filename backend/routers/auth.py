# routers/auth.py
from fastapi import Header, HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from passlib.hash import pbkdf2_sha256
from jose import jwt, JWTError, ExpiredSignatureError
from pydantic import ValidationError

from models.auth import Login
from tables import Student, Teacher
from db import get_db
from env import secret_key

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
    redirect_slashes=True,
)

@router.post("/login")
async def login(login_info: Login, db: Session = Depends(get_db)):
    """
    Login as a teacher or student with username/password
    """
    teacher = db.query(Teacher).filter(Teacher.email == login_info.email).first()
    student = db.query(Student).filter(Student.email == login_info.email).first()

    found_user, user_type = (teacher, "teacher") if teacher else ((student, "student") if student else (None, None))

    # Support both hashed and legacy plaintext (temporary)
    authenticated = False
    if found_user and found_user.password:
        try:
            authenticated = pbkdf2_sha256.verify(login_info.password, found_user.password)
        except ValueError:
            # Not a hash? fall back to equality check (legacy)
            authenticated = (login_info.password == found_user.password)

    if authenticated:
        claims = {"email": found_user.email, "name": found_user.name, "id": found_user.id, "type": user_type}
        access_token = jwt.encode(claims, secret_key, algorithm="HS256")
        return {
            "message": f"Successfully logged in {found_user.name}",
            "access_token": access_token,
            **claims,
        }
    else:
        raise HTTPException(status_code=404, detail="User login info not valid")

def jwt_token_verification(access_token: str = Header()):
    try:
        return jwt.decode(access_token, secret_key, algorithms=["HS256"])
    except ExpiredSignatureError:
        raise HTTPException(status_code=409, detail="The JWT submitted is expired. Please login again")
    except JWTError:
        raise HTTPException(status_code=401, detail="The JWT submitted is invalid")

def get_user_from_id(user_id: int, user_type: str, db: Session):
    if user_type == "teacher":
        user = db.query(Teacher).filter(Teacher.id == user_id).first()
    elif user_type == "student":
        user = db.query(Student).filter(Student.id == user_id).first()
    else:
        raise HTTPException(status_code=404, detail="User type not recognized")
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def get_current_user(access_token: str = Header(), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(access_token, secret_key, algorithms=["HS256"])
        user_id = payload.get("id"); user_type = payload.get("type")
        if user_id is None or user_type is None:
            raise HTTPException(status_code=403, detail="Invalid token")
        return get_user_from_id(user_id, user_type, db)
    except (JWTError, ValidationError):
        raise HTTPException(status_code=403, detail="Could not validate credentials")
