"""empty message

Revision ID: 0bcdd401ed55
Revises: ebaca274f3e4
Create Date: 2025-06-06 17:41:14.154559

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0bcdd401ed55'
down_revision: Union[str, None] = 'ebaca274f3e4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
