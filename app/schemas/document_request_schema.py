from pydantic import BaseModel
from typing import Literal

class DocumentRequestCreate(BaseModel):
    document_type_name: str
    purpose: str | None = None
    class Config:
        from_attributes=True

class DocumentRequestUpdate(BaseModel):
    purpose: str | None = None
    status: Literal["cancelled"] | None = None
    class Config:
        from_attributes=True

class DocumentRequestStatusUpdate(BaseModel):
    status: Literal[
        "approved",
        "rejected"
    ]
    class Config:
        from_attributes=True

class DocumentRequestShow(BaseModel):
    document_request_id:int
    employee_code: str
    full_name:str
    designation:str
    department_name:str
    document_type_name: str
    purpose: str | None
    status: str
    class Config:
        from_attributes=True