"""Adjusted model

Revision ID: b67afe9b9ccd
Revises: 5c13739f730b
Create Date: 2023-09-10 22:24:39.114408

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "b67afe9b9ccd"
down_revision: Union[str, None] = "5c13739f730b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("expense_participants")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "expense_participants",
        sa.Column("user_id", sa.UUID(), autoincrement=False, nullable=False),
        sa.Column("expense_id", sa.UUID(), autoincrement=False, nullable=False),
        sa.Column(
            "created_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=True
        ),
        sa.Column(
            "modified_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=True
        ),
        sa.Column("created_by", sa.UUID(), autoincrement=False, nullable=True),
        sa.Column("modified_by", sa.UUID(), autoincrement=False, nullable=True),
        sa.ForeignKeyConstraint(
            ["created_by"], ["users.id"], name="expense_participants_created_by_fkey"
        ),
        sa.ForeignKeyConstraint(
            ["expense_id"], ["expenses.id"], name="expense_participants_expense_id_fkey"
        ),
        sa.ForeignKeyConstraint(
            ["modified_by"], ["users.id"], name="expense_participants_modified_by_fkey"
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name="expense_participants_user_id_fkey"
        ),
        sa.PrimaryKeyConstraint(
            "user_id", "expense_id", name="expense_participants_pkey"
        ),
    )
    # ### end Alembic commands ###
