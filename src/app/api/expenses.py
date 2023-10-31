from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.services import expense_service
from typing import List
from uuid import UUID
from src.app.models import User
from src.app.schemas import expense
from src.database import get_db
from src.app.api.users import get_current_user

router = APIRouter()

@router.post("/expenses/", response_model=expense.Expense)
async def create_new_expense(expense_data: expense.ExpenseCreate, _: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    db_expense = await expense_service.create_expense(db=db, expense=expense_data)
    
    # Convert the ORM Expense object to the Pydantic Expense model
    return expense.Expense(
        id=db_expense.id,
        name=db_expense.name,
        hangout_id=db_expense.hangout_id,
        amount=db_expense.amount,
        shared_by=[user.id for user in db_expense.shared_by],
        created_at=db_expense.created_at,
        modified_at=db_expense.modified_at
    )

@router.get("/hangouts/{hangout_id}/expenses/", response_model=List[expense.Expense])
async def list_expenses_for_hangout(hangout_id: UUID, _: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    db_expenses = await expense_service.get_expenses_for_hangout(db, hangout_id=hangout_id)
    
    # Transform each ORM Expense object to a Pydantic Expense model
    transformed_expenses = []
    for db_expense in db_expenses:
        transformed_expenses.append(
            expense.Expense(
                id=db_expense.id,
                name=db_expense.name,
                hangout_id=db_expense.hangout_id,
                amount=db_expense.amount,
                shared_by=[user.email for user in db_expense.shared_by],
                created_at=db_expense.created_at,
                modified_at=db_expense.modified_at
            )
        )
    
    return transformed_expenses

