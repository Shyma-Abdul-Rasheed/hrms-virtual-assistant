from app.db.connections import Base
from sqlalchemy import Column,Integer,String,DateTime,Boolean,ForeignKey,func,text
from sqlalchemy.orm import relationship
from datetime import datetime

class DocumentRequest(Base):
    __tablename__="hr_document_requests"
    document_request_id=Column(Integer,primary_key=True,index=True)
    employee_id = Column(Integer,ForeignKey("employees.employee_id"),nullable=False)
    document_type_id=Column(Integer,ForeignKey("hr_document_types.document_type_id"),nullable=False)
    purpose=Column(String)
    status = Column(String,nullable=False,default="pending",server_default=text("'pending'"))
    requested_at=Column(DateTime,default=datetime.now,server_default=func.now())
    updated_at=Column(DateTime,default=datetime.now,server_default=func.now(),onupdate=func.now())

    employee=relationship("Employee",back_populates="document_request")
    document_type=relationship("DocumentType",back_populates="document_request")