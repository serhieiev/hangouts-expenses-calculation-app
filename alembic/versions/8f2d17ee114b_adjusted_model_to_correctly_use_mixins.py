"""Adjusted model to correctly use mixins

Revision ID: 8f2d17ee114b
Revises: b67afe9b9ccd
Create Date: 2023-09-10 22:58:12.913585

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8f2d17ee114b"
down_revision: Union[str, None] = "b67afe9b9ccd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("users_created_by_fkey", "users", type_="foreignkey")
    op.drop_constraint("users_modified_by_fkey", "users", type_="foreignkey")
    op.drop_column("users", "modified_by")
    op.drop_column("users", "created_by")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "users", sa.Column("created_by", sa.UUID(), autoincrement=False, nullable=True)
    )
    op.add_column(
        "users", sa.Column("modified_by", sa.UUID(), autoincrement=False, nullable=True)
    )
    op.create_foreign_key(
        "users_modified_by_fkey", "users", "users", ["modified_by"], ["id"]
    )
    op.create_foreign_key(
        "users_created_by_fkey", "users", "users", ["created_by"], ["id"]
    )
    # ### end Alembic commands ###
