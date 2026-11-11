from app.db.connections import Base
from sqlalchemy import Column,Integer,DateTime,ForeignKey,String,func,text
from sqlalchemy.orm import relationship
from datetime import datetime

class LeaveApproval(Base):
    __tablename__="leave_approvals"
    leave_approval_id=Column(Integer,primary_key=True,index=True)
    approver_id=Column(Integer,ForeignKey("employees.employee_id"),nullable=False)
    leave_request_id=Column(Integer,ForeignKey("leave_requests.leave_request_id"),nullable=False)
    decision=Column(String,nullable=False)
    comments=Column(String,nullable=True)
    approved_at=Column(DateTime,default=datetime.now,server_default=func.now())

    approver=relationship("Employee",back_populates="leave_approval")
    leave_request=relationship("LeaveRequest",back_populates="leave_approval")