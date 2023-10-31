from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from typing import List, Optional

class ExpenseBase(BaseModel):
    hangout_id: UUID
    name: str
    amount: int
    shared_by: Optional[List[str]]  # List of user UUIDs who share this expense

class ExpenseCreate(ExpenseBase):
    pass

class Expense(ExpenseBase):
    id: UUID
    created_at: datetime
    modified_at: datetime

    class Config:
        orm_mode = True
