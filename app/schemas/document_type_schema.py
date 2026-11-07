from pydantic import BaseModel

class DocumentTypeCreate(BaseModel):
    document_type_name:str
    description: str | None = None
    requires_hr_approval: bool = True
    is_active: bool = True
    class Config:
        from_attributes=True

class DocumentTypeUpdate(BaseModel):
    document_type_name: str | None = None
    description: str | None = None
    requires_hr_approval: bool | None = None
    is_active: bool | None = None
    class Config:
        from_attributes=True

class DocumentTypeShow(BaseModel):
    document_type_name: str
    description: str | None
    requires_hr_approval: bool
    is_active: bool
    class Config:
        from_attributes=True

