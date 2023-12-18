from fastapi import HTTPException, APIRouter
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
from models.test import CreateTest, UpdateTest, GetTest
from tables import Test
from db import get_db, session
import base64
from time import sleep

router = APIRouter(
    prefix="/test",
    tags=["test"],
    responses={404: {"description": "Test: Not found"}},
    redirect_slashes=True
)

@router.post("/") #, #dependencies=[Depends(jwt_token_verification)])
def create_test(test: CreateTest):
    try:
        answer_key = base64.b64decode(test.answer_key.encode("utf-8"))

        print(f"""{type(test.name)}{type(test.start_t)}{type(test.end_t)}
{type(test.num_questions)}{type(answer_key)}{type(test.course_id)}""")

        temp = Test(name=test.name, start_t=test.start_t, end_t=test.end_t, 
                    num_questions=test.num_questions, answer_key=answer_key, course_id=test.course_id)
        session.add(temp)
        session.commit()
    except IntegrityError as e:
        print(f"Error createtest: {e}")
        session.rollback()
        raise HTTPException(status_code=400, detail="Test with this ID already exists")

    return test

@router.get("/", response_model=List[GetTest])
def get_all_tests():
    tests = session.query(Test).all()
    print(f"Tests: {tests}")
    # returnable = [test for test in tests]
    try:
        print(f"answer_key: {type(tests[0].answer_key)}")
        for test in tests:
            test.answer_key = base64.b64encode(test.answer_key).decode("utf8")
        print(f"answer_key: {type(tests[0].answer_key)}")
 
        
        sleep(8)
        return tests

    except EncodingWarning:
        raise HTTPException(500, detail="Binary decoding warning...")
    finally:
        session.rollback()

@router.get("/{test_id}/", response_model=GetTest)
def get_test_by_id(test_id: int, db: Session = Depends(get_db)):
    test = db.query(Test).filter(Test.id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    
    return test

@router.put("/{test_id}/")
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

@router.delete("/{test_id}/")
def delete_test(test_id: int, db: Session = Depends(get_db)):
    test = db.query(Test).filter(Test.id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    
    db.delete(test)
    db.commit()
    
    return {"message": "Test deleted successfully"}

    