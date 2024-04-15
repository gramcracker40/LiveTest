"""
implements the pydantic models required for the 'test' router
"""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, Json
from typing_extensions import Annotated

class GetTestMinimum(BaseModel):
    id: str
    name: str
    

class CreateTest(BaseModel):
    name: str
    start_t: datetime
    end_t: datetime
    num_questions: int = Field(..., ge=1, le=200)  # Number of questions must be between 0 and 200
    num_choices: int = Field(..., ge=2, le=7)
    course_id: int
    answers: dict


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
    num_choices: int
    course_id: int


class CreateTestConfirmation(BaseModel):
    id: str
    name: str


class GetTestImage(BaseModel):
    pass


class ListTests(BaseModel):
    tests: List[GetTest]
