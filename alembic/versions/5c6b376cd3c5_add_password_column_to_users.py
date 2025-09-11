"""Add password column to users

Revision ID: 5c6b376cd3c5
Revises: 6b7fc285bf6d
Create Date: 2025-09-11 12:59:30.995323

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5c6b376cd3c5'
down_revision: Union[str, Sequence[str], None] = '6b7fc285bf6d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add password column to users table
    op.add_column('users', sa.Column('password', sa.String(length=255), nullable=False, server_default=''))


def downgrade() -> None:
    # Remove password column
    op.drop_column('users', 'password')