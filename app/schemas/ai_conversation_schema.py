from pydantic import BaseModel
from typing import Literal
from datetime import datetime

class AIConversationStatusUpdate(BaseModel):
    status: Literal["active", "completed"]
    class Config:
        from_attributes=True

class AIConversationResponse(BaseModel):
    employee_id: int
    conversation_id: int
    status: str
    started_at: datetime
    ended_at: datetime | None
    class Config:
        from_attributes=True

