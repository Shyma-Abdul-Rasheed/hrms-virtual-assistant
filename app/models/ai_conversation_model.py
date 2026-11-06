from app.db.connections import Base
from sqlalchemy import Column,Integer,String,DateTime,Boolean,ForeignKey,func,text
from sqlalchemy.orm import relationship
from datetime import datetime

class AIConversation(Base):
    __tablename__="ai_conversations"
    conversation_id=Column(Integer,primary_key=True,index=True)
    employee_id = Column(Integer,ForeignKey("employees.employee_id"),nullable=False)
    status = Column(String,nullable=False,default="active",server_default=text("'active'"))
    started_at=Column(DateTime(timezone=True),nullable=False,server_default=func.now())
    ended_at=Column(DateTime(timezone=True),nullable=True)

    employee=relationship("Employee",back_populates="ai_conversation")
    ai_message=relationship("AIMessage",back_populates="ai_conversation")