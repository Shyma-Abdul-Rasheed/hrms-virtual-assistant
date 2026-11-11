from pydantic import BaseModel,Field

class LeaveTypeCreate(BaseModel):
    leave_type_name:str
    description:str
    is_paid:bool = True
    min_notice_days:int = Field(default=0, ge=0)
    class Config:
        from_attributes=True

class LeaveTypeUpdate(BaseModel):
    leave_type_name: str | None = None
    description: str | None = None
    is_paid: bool | None = None
    min_notice_days: int | None = Field(default=None, ge=0)
    class Config:
        from_attributes=True

class LeaveTypeShow(BaseModel):
    leave_type_id:int
    leave_type_name: str
    description: str
    is_paid: bool
    min_notice_days: int
    class Config:
        from_attributes=True

