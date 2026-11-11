from pydantic import BaseModel
from typing import Literal
from datetime import datetime

MessageSender = Literal["employee","Ava","hr","admin"]

class AIMessageCreate(BaseModel):
    conversation_id: int
    message_content: str

class AIMessageResponse(BaseModel):
    conversation_id: int
    sender: MessageSender
    message_content: str
    timestamp: datetime

