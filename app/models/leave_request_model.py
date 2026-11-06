from app.db.connections import Base
from sqlalchemy import Column,Integer,String,DateTime,ForeignKey,Date,Numeric,CheckConstraint,func,text
from sqlalchemy.orm import relationship
from datetime import datetime

class LeaveRequest(Base):
    __tablename__ = "leave_requests"

    leave_request_id = Column(Integer,primary_key=True,index=True)
    employee_id = Column(Integer,ForeignKey("employees.employee_id"),nullable=False)
    leave_type_id = Column(Integer,ForeignKey("leave_types.leave_type_id"),nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    days_requested = Column(Numeric(5, 2),nullable=False)
    reason = Column(String, nullable=True)
    status = Column(String,nullable=False,default="pending",server_default=text("'pending'"))
    created_at=Column(DateTime,default=datetime.now,server_default=func.now())
    updated_at=Column(DateTime,default=datetime.now,server_default=func.now(),onupdate=func.now())

    employee=relationship("Employee",back_populates="leave_request")
    leave_type=relationship("LeaveType",back_populates="leave_request")
    leave_approval=relationship("LeaveApproval",back_populates="leave_request")
