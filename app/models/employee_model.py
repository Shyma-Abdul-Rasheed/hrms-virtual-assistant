from app.db.connections import Base
from sqlalchemy import Column, ForeignKey,Integer,String,DateTime,Boolean,Enum as SQLEnum,text,func
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum

class Roles(str,Enum):
    employee='employee'
    hr='hr'
    admin='admin'
    manager='manager'

class Employee(Base):
    __tablename__="employees"
    employee_id=Column(Integer,primary_key=True,index=True)
    employee_code=Column(String,nullable=False,unique=True,server_default=text(
        "'EMP' || LPAD(nextval('employee_code_seq')::text, 3, '0')"
    ))
    full_name=Column(String,nullable=False)
    email=Column(String,nullable=False,unique=True)
    hashed_password=Column(String)
    department_id=Column(Integer,ForeignKey("departments.department_id"),nullable=False)
    designation=Column(String,nullable=False)
    role=Column(SQLEnum(Roles,name='role',create_type=False),nullable=False)
    is_active=Column(Boolean,nullable=False,default=True,server_default=text("true"))
    created_at=Column(DateTime,default=datetime.now,server_default=func.now())
    updated_at=Column(DateTime,default=datetime.now,server_default=func.now(),onupdate=func.now())

    department=relationship("Department",back_populates="employee")
    leave_balance=relationship("LeaveBalance",back_populates="employee")
    leave_request=relationship("LeaveRequest",back_populates="employee")
    leave_approval=relationship("LeaveApproval",back_populates="approver")
    document_request=relationship("DocumentRequest",back_populates="employee")
    ai_conversation=relationship("AIConversation",back_populates="employee")