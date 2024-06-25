from fastapi import HTTPException, APIRouter
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
from models.users import GetStudentMinimum
from answer_sheets import Pictron
from tables import Test, Course
from db import session, compress_data, compress_image
import base64
from time import sleep

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
        # #TODO check to see that the user_type and user_id of the JWT 
    # making the call is the teacher that teaches the course

    # query the course and make sure it exists. 
    course = session.query(Course).get(test.course_id)

    if not course:
        raise HTTPException(404, detail=f"course does not exist.")
    

    new_test = Test(**test.model_dump())

    # find the best template for the given number of questions and choices. 
    answer_sheet_config = Pictron.find_best_config(test.num_questions, test.num_choices, api=True)
    answer_sheet = Pictron(**answer_sheet_config)
    
    # generate, compress, and save the blank version image of the test
    answer_sheet.generate(course_name=course.name, test_name=test.name)
    # answer_sheet.image.show(title=f"Blank test: {test.name}") # debug
    blank_bytes = io.BytesIO()
    answer_sheet.image.save(blank_bytes, format="JPEG")
    new_test.answer_key_blank = compress_data(compress_image(blank_bytes.getvalue(), quality=30))
   
    # generate and save the compressed, filled in key version of the test
    answer_sheet.generate(
        answers={int(question_num): answer for question_num, answer in test.answers.items()}, 
        course_name=course.name, 
        test_name=test.name
    )
    #answer_sheet.image.show(title=f"Test Key: {test.name}") # debug
    filled_bytes = io.BytesIO()
    answer_sheet.image.save(filled_bytes, format="JPEG")
    new_test.answer_key_filled = compress_data(compress_image(filled_bytes.getvalue(), quality=30))

    # stringify the answers that were passed for storage in the database
    new_test.answers = json.dumps(test.answers)

    try:
        session.add(new_test)
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(409, detail=f"{course.name} already has a test named {test.name}")


    db_obj = session.query(Test).filter(Test.name == test.name, Test.course_id == test.course_id).first()
    return {"id": db_obj.id, "name": test.name}


# 
# @router.post("/882E", response_model=CreateTestConfirmation)  # , dependencies=[Depends(jwt_token_verification)])
# def create_test_882E(test: CreateTest):
#     '''
#     Create a test using a Form 882E
#     '''
#     try:
#         course = session.query(Course).get(test.course_id)
#         if not course:
#             raise HTTPException(400, detail=f"Course {test.course_id} does not exist.")
        
#         # start by generating the answer key
#         answer_key_bytes = base64.b64decode(test.answer_key.encode("utf-8"))
#         # answer_key = TestProcessor.generate_key(
#         #     test.num_questions, key_bytes=answer_key_bytes
#         # )
#         # print(f"Answer_key: {json.dumps(answer_key)}")
#         new_test = Test(
#             name=test.name,
#             start_t=test.start_t,
#             end_t=test.end_t,
#             num_questions=test.num_questions,
#             answer_key=answer_key_bytes,
#             course_id=test.course_id,
#             file_extension=test.file_extension,
#             # answers=json.dumps(answer_key),
#         )
#         session.add(new_test)
#         session.commit()
#     except IntegrityError as e:
#         print(f"Error create-test: {e}")
#         session.rollback()
#         raise HTTPException(status_code=400, detail="This test already exists")
#     except cv2.error as e:
#         print(str(e))
#         print("CV2 Error!!!")
#         session.rollback()
#         raise HTTPException(
#             status_code=400,
#             detail="There was an error processing this image, please submit a new one",
#         )

#     new_t = (
#         session.query(Test)
#         .filter(Test.name == test.name, Test.course_id == test.course_id)
#         .first()
#     )

#     return {"id": new_t.id, "name": new_t.name}


@router.get("/", response_model=List[GetTest])
def get_all_tests():
    tests = session.query(Test).all()
    if len(tests) == 0:
        return []

    return tests


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


@router.get("/image/key/{test_id}/")
def get_test_key_image(test_id: str):
    test = session.query(Test).get(test_id)

    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    
    return StreamingResponse(io.BytesIO(test.answer_key_filled), media_type="image/png")

@router.get("/image/blank/{test_id}/")
def get_test_blank_image(test_id: str):
    test = session.query(Test).get(test_id)

    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    
    return StreamingResponse(io.BytesIO(test.answer_key_blank), media_type="image/png")


@router.get("/image/blank/{num_questions}/{num_choices}/{course_id}")
async def get_test_blank_template(num_questions:int, 
                                  num_choices:int, 
                                  course_id:int,
                                  test_name:str=None):
    '''
    return a templated LiveTest generated answer sheet.
    '''
    best_config = Pictron.find_best_config(num_questions, num_choices)
    obj = Pictron(**best_config)

    course = session.query(Course).get(course_id)
    if not course:
        raise HTTPException(404, detail=f"course does not exist.")

    obj.generate(
        course_name=course.name, 
        test_name=test_name
    )

    filled_bytes = io.BytesIO()
    obj.image.save(filled_bytes, format="PNG")

    return StreamingResponse(io.BytesIO(filled_bytes.getvalue()), media_type="image/png")



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



@router.get("/students/{test_id}", response_model=List[GetStudentMinimum])
def get_not_submitted_for_test(test_id: str):
    '''
    grabs a list of students that are yet to submit for a particular test
    '''
    test = session.query(Test).get(test_id)

    if test is None:
        raise HTTPException(404, detail="Test not found")
    
    submitted = {x.student_id: None for x in test.submissions}
    not_submitted = [i.__dict__ for i in test.course.students if i.id not in submitted]

    return not_submitted

