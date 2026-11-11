from pydantic import BaseModel,Field
from typing import Literal
from datetime import datetime

class LeaveApprovalCreate(BaseModel):
    leave_request_id: int
    decision: Literal["approved", "rejected"]
    comments: str | None = None
    class Config:
            from_attributes=True

class LeaveApprovalUpdate(BaseModel):
      decision:Literal["approved", "rejected"] | None = None
      comments:str | None = None
      class Config:
        from_attributes=True


class LeaveApprovalResponse(BaseModel):
    full_name: str
    role:str
    leave_type_name:str
    leave_request_id: int
    decision: Literal["approved", "rejected"]
    comments: str | None
    approved_at:datetime
    class Config:
        from_attributes=True

