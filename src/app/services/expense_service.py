from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from src.app import models
from src.app.models import Expense, expense_shared_by
from src.app.services import hangout_service
from src.app.schemas.expense import ExpenseCreate
from src.app.schemas.hangout import HangoutDetails
from uuid import UUID



async def create_expense(db: AsyncSession, expense: ExpenseCreate) -> Expense:
    new_expense = Expense(
        hangout_id=expense.hangout_id,
        name = expense.name,
        amount=expense.amount,

    )
    db.add(new_expense)
    await db.commit()
    if expense.shared_by:
        for user_id in expense.shared_by:
            await db.execute(
                expense_shared_by.insert().values(
                    user_id=user_id, 
                    expense_id=new_expense.id
                )
            )
    await db.commit()
    # Refresh the expense and eagerly load shared_users
    result = await db.execute(
        select(Expense).options(joinedload(Expense.shared_by)).where(Expense.id == new_expense.id)
    )
    return result.scalar()


async def get_expenses_for_hangout(db: AsyncSession, hangout_id: UUID):
    result = await db.execute(
        select(Expense).options(joinedload(Expense.shared_by)).where(Expense.hangout_id == hangout_id)
    )
    return result.scalars().unique().all()


async def calculate_expenses_for_hangout(db: AsyncSession, hangout_id: UUID):
    hangout_details: HangoutDetails = await hangout_service.get_hangout_details(db, hangout_id)
    
    if not hangout_details:
        raise HTTPException(status_code=404, detail="Hangout not found")
    
    expenses = await get_expenses_for_hangout(db, hangout_id)
    
    # Initialize a dictionary to keep track of expenses per user
    user_expenses = {participant.id: 0 for participant in hangout_details.participants}

    # Calculate each user's total expense
    for expense in expenses:
        amount_per_user = expense.amount / len(expense.shared_by)
        for user_id in expense.shared_by:
            user_expenses[user_id.id] += amount_per_user
    
    # Now we can construct a summary of expenses
    expenses_summary = {
    "total_expenses": 0,
    "individual_expenses_summary": {},
    "expenses_by_user": {}
}

    for expense in expenses:
        expense_id_str = str(expense.id)
        expenses_summary["individual_expenses_summary"][expense_id_str] = {
            "name": expense.name,
            "total_amount": expense.amount
        }
        
        split_amount = expense.amount / len(expense.shared_by)
        for user in expense.shared_by:
            user_id_str = str(user.id)
            if user_id_str not in expenses_summary["expenses_by_user"]:
                expenses_summary["expenses_by_user"][user_id_str] = {
                    "email": user.email,
                    "total_expense": 0,
                    "individual_expenses": []
                }
            user_expense_info = expenses_summary["expenses_by_user"][user_id_str]
            user_expense_info["total_expense"] += split_amount
            user_expense_info["individual_expenses"].append({
                "expense_id": expense_id_str,
                "name": expense.name,
                "amount": split_amount
            })
        expenses_summary["total_expenses"] += expense.amount
        

    return expenses_summary
