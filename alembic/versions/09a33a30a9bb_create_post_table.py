"""Create post table

Revision ID: 09a33a30a9bb
Revises: 
Create Date: 2025-11-05 08:46:32.890735

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '09a33a30a9bb'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("post",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("published", sa.Boolean(), server_default="TRUE", nullable=False)
    )
    


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("post")
