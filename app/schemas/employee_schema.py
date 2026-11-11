from pydantic import BaseModel, EmailStr
from enum import Enum

class Roles(str,Enum):
    employee='employee'
    hr='hr'
    admin='admin'
    manager='manager'

class EmployeeCreate(BaseModel):
    full_name:str
    email:EmailStr
    department_name:str
    designation:str
    role:Roles
    class Config:
        from_attributes=True

class EmployeeUpdate(BaseModel):
    full_name:str | None = None
    email:str | None = None
    department_name:str | None = None
    designation:str | None = None
    role:Roles | None = None
    is_active:bool | None = None
    class Config:
        from_attributes=True

class EmployeeSignup(BaseModel):
    full_name:str
    email:EmailStr
    password:str
    class Config:
        from_attributes=True

class EmployeeLogin(BaseModel):
    email:EmailStr
    password:str
    class Config:
        from_attributes=True

class EmployeeShow(BaseModel):
    employee_id:int
    employee_code:str
    full_name:str
    email:EmailStr
    department_name:str
    designation:str
    role:Roles
    is_active:bool
    class Config:
        from_attributes=True

