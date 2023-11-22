from pydantic import BaseModel

class Login(BaseModel): 
    email: str
    password: str

class CreateTeacher(BaseModel):
    name: str 
    email: str
    password: str

class CreateStudent(CreateTeacher):
    M_number: str

class UpdateTeacher(BaseModel):
    email: str
    password: str

class UpdateStudent(UpdateTeacher):
    pass

class GetTeacher(BaseModel):
    name: str
    email: str

class GetStudent(GetTeacher):
    pass
    
