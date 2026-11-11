from app.db.connections import Base
from sqlalchemy import Column,Integer,String,DateTime,Boolean,ForeignKey,func,text
from sqlalchemy.orm import relationship
from datetime import datetime

class AIMessage(Base):
    __tablename__="ai_messages"
    message_id=Column(Integer,primary_key=True,index=True)
    conversation_id = Column(Integer,ForeignKey("ai_conversations.conversation_id"),nullable=False)
    sender = Column(String)
    message_content=Column(String)
    timestamp=Column(DateTime,default=datetime.now,server_default=func.now())

    ai_conversation=relationship("AIConversation",back_populates="ai_message")