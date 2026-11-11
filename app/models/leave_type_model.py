from app.db.connections import Base
from sqlalchemy import Column,Integer,String,DateTime,Boolean,func,text
from sqlalchemy.orm import relationship
from datetime import datetime

class LeaveType(Base):
    __tablename__="leave_types"
    leave_type_id=Column(Integer,primary_key=True,index=True)
    leave_type_name=Column(String,nullable=False,unique=True)
    description=Column(String,nullable=False)
    is_paid=Column(Boolean,nullable=False,default=True,server_default=text("true"))
    min_notice_days=Column(Integer,nullable=False,default=0,server_default="0")
    created_at=Column(DateTime,default=datetime.now,server_default=func.now())
    updated_at=Column(DateTime,default=datetime.now,server_default=func.now(),onupdate=func.now())

    leave_balance=relationship("LeaveBalance",back_populates="leave_type")
    leave_request=relationship("LeaveRequest",back_populates="leave_type")