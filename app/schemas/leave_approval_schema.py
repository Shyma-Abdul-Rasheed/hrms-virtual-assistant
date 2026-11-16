from pydantic import BaseModel,Field
from typing import Literal
from datetime import datetime,date
from decimal import Decimal

class LeaveApprovalCreate(BaseModel):
    leave_request_id: int
    decision: Literal["approved", "rejected"]
    comments: str | None = None
    class Config:
            from_attributes=True

class LeaveApprovalShow(BaseModel):
    leave_approval_id:int
    employee_code:str
    full_name: str
    department_name:str
    leave_type_name:str
    start_date:date
    end_date:date
    days_requested:Decimal
    reason:str
    decision: Literal["approved", "rejected"]
    comments: str | None
    approved_by:str
    designation:str
    approved_at:datetime
    class Config:
        from_attributes=True

