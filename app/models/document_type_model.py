from app.db.connections import Base
from sqlalchemy import Column,Integer,String,DateTime,Boolean,func,text
from sqlalchemy.orm import relationship
from datetime import datetime

class DocumentType(Base):
    __tablename__="hr_document_types"
    document_type_id=Column(Integer,primary_key=True,index=True)
    document_type_name=Column(String,nullable=False,unique=True)
    description=Column(String)
    requires_hr_approval=Column(Boolean,nullable=False,default=True,server_default=text("true"))
    is_active=Column(Boolean,nullable=False,default=True,server_default=text("true"))
    created_at=Column(DateTime,default=datetime.now,server_default=func.now())
    updated_at=Column(DateTime,default=datetime.now,server_default=func.now(),onupdate=func.now())

    document_request=relationship("DocumentRequest",back_populates="document_type")