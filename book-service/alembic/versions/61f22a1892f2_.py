"""empty message

Revision ID: 61f22a1892f2
Revises: a835729a94e4
Create Date: 2025-06-06 17:44:34.718847

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '61f22a1892f2'
down_revision: Union[str, None] = 'a835729a94e4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
