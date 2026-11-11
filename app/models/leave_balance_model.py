from app.db.connections import Base
from sqlalchemy import Column,Integer,DateTime,ForeignKey,Computed,func,text
from sqlalchemy.orm import relationship
from datetime import datetime

class LeaveBalance(Base):
    __tablename__="leave_balances"

    leave_balance_id=Column(Integer,primary_key=True,index=True)
    employee_id=Column(Integer,ForeignKey("employees.employee_id"),nullable=False)
    leave_type_id=Column(Integer,ForeignKey("leave_types.leave_type_id"),nullable=False)
    year=Column(Integer,nullable=False)
    entitlement_days=Column(Integer,nullable=False)
    used_days=Column(Integer,nullable=False,default=0,server_default=text("0"))
    balance_days=Column(Integer,Computed("entitlement_days - used_days"),nullable=False)
    created_at=Column(DateTime,default=datetime.now,server_default=func.now())
    updated_at=Column(DateTime,default=datetime.now,server_default=func.now(),onupdate=func.now())

    employee=relationship("Employee",back_populates="leave_balance")
    leave_type=relationship("LeaveType",back_populates="leave_balance")