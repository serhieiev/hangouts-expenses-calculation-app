"""Initial migration

Revision ID: 5c13739f730b
Revises: 
Create Date: 2023-09-09 02:31:16.424661

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5c13739f730b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'comments', ['id'])
    op.create_unique_constraint(None, 'expenses', ['id'])
    op.create_unique_constraint(None, 'hangouts', ['id'])
    op.create_unique_constraint(None, 'users', ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_constraint(None, 'hangouts', type_='unique')
    op.drop_constraint(None, 'expenses', type_='unique')
    op.drop_constraint(None, 'comments', type_='unique')
    # ### end Alembic commands ###
