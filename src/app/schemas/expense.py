from pydantic import BaseModel, EmailStr
from datetime import datetime
from uuid import UUID
from typing import List, Dict, Optional

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

class UserExpense(BaseModel):
    email: str
    total_expense: int

class ExpenseDetail(BaseModel):
    name: str
    total_amount: int

class ExpenseSummary(BaseModel):
    total_expenses: int
    expenses_by_user: Dict[UUID, UserExpense]
    individual_expenses_summary: Dict[str, ExpenseDetail]

    class Config:
        orm_mode = True
