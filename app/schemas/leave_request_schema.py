from pydantic import BaseModel,Field
from datetime import date,datetime
from decimal import Decimal
from typing import Literal


LeaveRequestStatus = Literal[
    "pending",
    "approved",
    "rejected",
    "cancelled"
]

class LeaveRequestCreate(BaseModel):
    leave_type_name: str
    start_date: date
    end_date: date
    days_requested: Decimal = Field(gt=0)
    reason: str | None = None
    class Config:
        from_attributes=True

class LeaveRequestUpdate(BaseModel):
    leave_type_name: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    days_requested: Decimal | None = Field(default=None, gt=0)
    reason: str | None = None
    status: Literal["cancelled"] | None = None
    class Config:
        from_attributes=True

class LeaveRequestShow(BaseModel):
    employee_code: str
    full_name:str
    leave_type_name: str
    start_date: date
    end_date: date
    days_requested: Decimal
    reason: str | None
    status: LeaveRequestStatus
    submitted_at:datetime
    class Config:
        from_attributes=True

