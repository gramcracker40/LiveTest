from fastapi import HTTPException, APIRouter
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
import json
import cv2
import io
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
from models.test import (
    CreateTest,
    UpdateTest,
    GetTest,
    CreateTestConfirmation,
    GetTests,
)
from tables import Test, Course
from db import get_db, session
import base64
from time import sleep
# from core.TestProcessor import TestProcessor

router = APIRouter(
    prefix="/test",
    tags=["test"],
    responses={404: {"description": "Test: Not found"}},
    redirect_slashes=True,
)


@router.post("/", response_model=CreateTestConfirmation)  # , dependencies=[Depends(jwt_token_verification)])
def create_test_live(test: CreateTest):
    '''
    Create a test using the offical LiveTest answer sheets
    '''


@router.post("/882E", response_model=CreateTestConfirmation)  # , dependencies=[Depends(jwt_token_verification)])
def create_test_882E(test: CreateTest):
    '''
    Create a test using a Form 882E
    '''
    try:
        course = session.query(Course).get(test.course_id)
        if not course:
            raise HTTPException(400, detail=f"Course {test.course_id} does not exist.")
        
        # start by generating the answer key
        answer_key_bytes = base64.b64decode(test.answer_key.encode("utf-8"))
        # answer_key = TestProcessor.generate_key(
        #     test.num_questions, key_bytes=answer_key_bytes
        # )
        # print(f"Answer_key: {json.dumps(answer_key)}")
        new_test = Test(
            name=test.name,
            start_t=test.start_t,
            end_t=test.end_t,
            num_questions=test.num_questions,
            answer_key=answer_key_bytes,
            course_id=test.course_id,
            file_extension=test.file_extension,
            # answers=json.dumps(answer_key),
        )
        session.add(new_test)
        session.commit()
    except IntegrityError as e:
        print(f"Error create-test: {e}")
        session.rollback()
        raise HTTPException(status_code=400, detail="This test already exists")
    except cv2.error as e:
        print(str(e))
        print("CV2 Error!!!")
        session.rollback()
        raise HTTPException(
            status_code=400,
            detail="There was an error processing this image, please submit a new one",
        )

    new_t = (
        session.query(Test)
        .filter(Test.name == test.name, Test.course_id == test.course_id)
        .first()
    )

    return {"id": new_t.id, "name": new_t.name}


@router.get("/", response_model=List[GetTest])
def get_all_tests():
    tests = session.query(Test).all()
    if len(tests) == 0:
        return []

    try:
        for test in tests:
            test.answer_key = base64.b64encode(test.answer_key).decode("utf8")

        return tests
    except EncodingWarning:
        raise HTTPException(500, detail="Binary decoding warning...")
    finally:
        session.rollback()


@router.get("/{test_id}/", response_model=GetTest)
def get_test_by_id(test_id: str):
    test = session.query(Test).filter(Test.id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    
    return test


@router.get("/course/{course_id}/", response_model=List[GetTests])
def get_tests_for_course(course_id: int):
    course = session.query(Course).filter_by(id=course_id).first()

    if not course:
        raise HTTPException(404, detail=f"Course {course_id} does not exist...")

    return course.tests


@router.get("/image/{test_id}")
def get_test_key_image(test_id: str):
    test = session.query(Test).get(test_id)

    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    
    return StreamingResponse(io.BytesIO(test.answer_key), media_type="image/jpg")


@router.patch("/{test_id}/")
def update_test(test_id: str, update_data: UpdateTest):
    test = session.query(Test).get(test_id)

    if not test:
        raise HTTPException(status_code=404, detail="Test not found")

    for key, value in update_data.model_dump().items():
        if value != None:
            setattr(test, key, value)

    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            400,
            detail=f"""A test named 
{update_data.name} already exists in this course""",
        )

    return {"detail": "Successfully updated test details."}


@router.delete("/{test_id}/")
def delete_test(test_id: str):
    test = session.query(Test).get(test_id)
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")

    name = test.name
    session.delete(test)
    session.commit()

    return {"detail": f"Test {name} deleted successfully"}
