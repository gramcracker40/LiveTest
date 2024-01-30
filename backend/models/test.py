"""
implements the pydantic models required for the 'test' router
"""
from datetime import datetime
from typing import List
from pydantic import BaseModel, StringConstraints
from typing_extensions import Annotated
from typing import Optional

class GetTestMinimum(BaseModel):
    id: str
    name: str
    

class CreateTest(BaseModel):
    name: str
    start_t: datetime
    end_t: datetime
    num_questions: int
    answer_key: str
    file_extension: Annotated[str, StringConstraints(pattern=r'^(jpg|png)$')]
    course_id: int


class UpdateTest(BaseModel):
    start_t: Optional[datetime] = None
    end_t: Optional[datetime] = None
    name: Optional[str] = None


class GetTests(BaseModel):
    start_t: datetime
    end_t: datetime
    id: str
    name: str
    

class GetTest(BaseModel):
    id: str
    name: str
    start_t: datetime
    end_t: datetime
    num_questions: int
    course_id: int


class CreateTestConfirmation(BaseModel):
    id: str
    name: str


class GetTestImage(BaseModel):
    pass


class ListTests(BaseModel):
    tests: List[GetTest]
