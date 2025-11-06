"""Add new Content column to Post table

Revision ID: f149f43b6ab4
Revises: 09a33a30a9bb
Create Date: 2025-11-05 08:59:07.917230

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f149f43b6ab4'
down_revision: Union[str, Sequence[str], None] = '09a33a30a9bb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('post', sa.Column('content', sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('post', 'content')
