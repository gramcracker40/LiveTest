'''
implements the models required for the 'test' router
'''
from datetime import datetime
from typing import List
from pydantic import BaseModel

class CreateTest(BaseModel):
    name: str
    start_t: datetime
    end_t: datetime
    num_questions: int
    answer_key: str
    course_id: int

class UpdateTest(BaseModel):
    start_t: datetime
    end_t: datetime
    num_questions: int
    answer_key: bytes

class GetTest(BaseModel):
    id: str
    name: str
    start_t: datetime
    end_t: datetime
    num_questions: int
    answer_key: str
    course_id: int

class ListTests(BaseModel):
    tests: List[GetTest]
