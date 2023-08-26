"""Create book table

Revision ID: 0001c564ef35
Revises: 
Create Date: 2023-08-26 12:46:16.175341

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0001c564ef35'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'books',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('author', sa.String(), nullable=False),
        sa.Column('date_of_release', sa.Date(), nullable=False),
        sa.Column('description', sa.String(), nullable=False),
        sa.Column('genre', sa.String(), nullable=False)
    )


def downgrade():
    op.drop_table('books')
