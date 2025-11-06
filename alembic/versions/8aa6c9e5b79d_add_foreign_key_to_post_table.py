"""Add foreign key to post table

Revision ID: 8aa6c9e5b79d
Revises: 8936be6bdce9
Create Date: 2025-11-05 23:55:13.132787

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8aa6c9e5b79d'
down_revision: Union[str, Sequence[str], None] = '8936be6bdce9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('post', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table='post', referent_table='users', local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('post_users_fk', table_name='post')
    op.drop_column('post', 'owner_id')
    pass
