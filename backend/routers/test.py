from fastapi import HTTPException, APIRouter
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
from models.test import CreateTest, UpdateTest, GetTest
from tables import Test
from db import session
from jwt import jwt_token_verification
from db import session, get_db

router = APIRouter(
    prefix="/test",
    tags=["test"],
    responses={404: {"description": "Test: Not found"}},
)

@router.post("/") #, #dependencies=[Depends(jwt_token_verification)])
def create_test(test: CreateTest, db: Session = Depends(get_db)):
    try:
        temp = Test(start_t=test.start_t, end_t=test.end_t, num_questions=test.num_questions, answer_key=test.answer_key, course_id=test.course_id)
        db.add(temp)
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Test with this ID already exists")

    return test

@router.get("/", response_model=List[GetTest])
def get_all_tests(db: Session = Depends(get_db)):
    tests = db.query(Test).all()
    return tests

@router.get("/{test_id}", response_model=GetTest)
def get_test_by_id(test_id: int, db: Session = Depends(get_db)):
    test = db.query(Test).filter(Test.id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    
    return test

@router.put("/{test_id}")
def update_test(test_id: int, update_data: UpdateTest, db: Session = Depends(get_db)):
    test = db.query(Test).filter(Test.id == test_id).first()
    
    # make sure it found one
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")

    test.start_t = update_data.start_t
    test.end_t = update_data.end_t
    test.num_questions = update_data.num_questions
    test.answer_key = update_data.answer_key
    
    db.commit()
    
    return test

@router.delete("/{test_id}")
def delete_test(test_id: int, db: Session = Depends(get_db)):
    test = db.query(Test).filter(Test.id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    
    db.delete(test)
    db.commit()
    
    return {"message": "Test deleted successfully"}

    