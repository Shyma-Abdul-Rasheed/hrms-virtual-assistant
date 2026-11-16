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
    full_name: str
    department_name:str
    leave_type_name:str
    start_date:date
    end_date:date
    requested_days:Decimal
    decision: Literal["approved", "rejected"]
    comments: str | None
    approved_at:datetime
    class Config:
        from_attributes=True

