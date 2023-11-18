from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from src.app.models import Expense, expense_shared_by
from src.app.schemas.expense import (
    ExpenseCreate,
    IndividualExpense,
    ExpenseDetail,
    ExpenseSummary,
    UserExpense,
)
from uuid import UUID


async def create_expense(db: AsyncSession, expense: ExpenseCreate) -> Expense:
    new_expense = Expense(
        hangout_id=expense.hangout_id,
        name=expense.name,
        amount=expense.amount,
    )
    db.add(new_expense)
    await db.commit()
    if expense.shared_by:
        for user_id in expense.shared_by:
            await db.execute(
                expense_shared_by.insert().values(
                    user_id=user_id, expense_id=new_expense.id
                )
            )
    await db.commit()
    # Refresh the expense and eagerly load shared_users
    result = await db.execute(
        select(Expense)
        .options(joinedload(Expense.shared_by))
        .where(Expense.id == new_expense.id)
    )
    return result.scalar()


async def get_expenses_for_hangout(db: AsyncSession, hangout_id: UUID):
    result = await db.execute(
        select(Expense)
        .options(joinedload(Expense.shared_by))
        .where(Expense.hangout_id == hangout_id)
    )
    return result.scalars().unique().all()


async def calculate_expenses_for_hangout(db: AsyncSession, hangout_id: UUID):
    # Query to get expenses for the hangout
    result = await db.execute(
        select(Expense)
        .options(joinedload(Expense.shared_by))
        .where(Expense.hangout_id == hangout_id)
    )
    expenses = result.scalars().unique().all()

    # Initialize the expenses summary
    expenses_summary = {
        "total_expenses": 0,
        "individual_expenses_summary": {},
        "expenses_by_user": {},
    }

    # Process each expense
    for expense in expenses:
        expense_id_str = str(expense.id)
        split_amount = expense.amount / len(expense.shared_by)

        # Update individual expenses summary
        expenses_summary["individual_expenses_summary"][expense_id_str] = {
            "name": expense.name,
            "total_amount": expense.amount,
        }

        # Update expenses by user
        for user in expense.shared_by:
            user_id_str = str(user.id)
            if user_id_str not in expenses_summary["expenses_by_user"]:
                expenses_summary["expenses_by_user"][user_id_str] = {
                    "email": user.email,
                    "total_expense": 0,
                    "individual_expenses": [],
                }
            user_expense_info = expenses_summary["expenses_by_user"][user_id_str]
            user_expense_info["total_expense"] += split_amount
            user_expense_info["individual_expenses"].append(
                {
                    "expense_id": expense_id_str,
                    "name": expense.name,
                    "amount": split_amount,
                }
            )

        # Update total expenses
        expenses_summary["total_expenses"] += expense.amount

    # Transform the summary into the appropriate model format
    for user_id, user_expense in expenses_summary["expenses_by_user"].items():
        user_expense["individual_expenses"] = [
            IndividualExpense(**ie) for ie in user_expense["individual_expenses"]
        ]
        expenses_summary["expenses_by_user"][user_id] = UserExpense(**user_expense)

    for expense_id, expense_detail in expenses_summary[
        "individual_expenses_summary"
    ].items():
        expenses_summary["individual_expenses_summary"][expense_id] = ExpenseDetail(
            **expense_detail
        )

    return ExpenseSummary(**expenses_summary)
