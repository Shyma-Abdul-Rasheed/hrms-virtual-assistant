from pydantic import BaseModel

class DepartmentCreate(BaseModel):
    department_name:str
    class Config:
        from_attributes=True

class DepartmentUpdate(BaseModel):
    department_name:str | None = None
    is_active:bool | None = None
    class Config:
        from_attributes=True

class DepartmentShow(BaseModel):
    department_name:str
    is_active:bool
    class Config:
        from_attributes=True

