"""Add index to genre field

Revision ID: 4606ef13805f
Revises: 0001c564ef35
Create Date: 2023-08-26 13:35:22.438104

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4606ef13805f'
down_revision: Union[str, None] = '0001c564ef35'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_index('idx_genre', 'books', ['genre'], unique=False)

def downgrade():
    op.drop_index('idx_genre', 'books')
