from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from src.app import models
from src.app.models import Expense, expense_shared_by
from src.app.schemas.expense import ExpenseCreate
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


