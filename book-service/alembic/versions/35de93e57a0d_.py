"""empty message

Revision ID: 35de93e57a0d
Revises: 61f22a1892f2
Create Date: 2025-06-06 17:46:57.191525

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '35de93e57a0d'
down_revision: Union[str, None] = '61f22a1892f2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('books', sa.Column('no_count', sa.Float(), nullable=True))
    op.add_column('books', sa.Column('two_count', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('books', 'two_count')
    op.drop_column('books', 'no_count')
    # ### end Alembic commands ###
