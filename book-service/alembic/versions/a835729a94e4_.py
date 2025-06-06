"""empty message

Revision ID: a835729a94e4
Revises: 0bcdd401ed55
Create Date: 2025-06-06 17:43:32.027630

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a835729a94e4'
down_revision: Union[str, None] = '0bcdd401ed55'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
