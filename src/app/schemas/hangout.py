from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from typing import List, Optional
from src.app.schemas import user

class HangoutBase(BaseModel):
    location: str
    time: datetime
    notes: Optional[str]

class HangoutCreate(HangoutBase):
    participants: Optional[List[UUID]]  # List of user UUIDs

class Hangout(HangoutBase):
    id: UUID
    # participants: Optional[List[UUID]]

class HangoutDetails(Hangout):
    organizer: user.UserResponse
    participants: List[user.UserResponse]

    class Config:
        orm_mode = True
        from_attributes = True
