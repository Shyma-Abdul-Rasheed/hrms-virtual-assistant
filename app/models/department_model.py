from app.db.connections import Base
from sqlalchemy import Column,Integer,String,DateTime,Boolean,func,text
from sqlalchemy.orm import relationship
from datetime import datetime

class Department(Base):
    __tablename__="departments"
    department_id=Column(Integer,primary_key=True,index=True)
    department_name=Column(String,nullable=False,unique=True)
    is_active=Column(Boolean,nullable=False,default=True,server_default=text("true"))
    created_at=Column(DateTime,default=datetime.now,server_default=func.now())

    employee=relationship("Employee",back_populates="department")