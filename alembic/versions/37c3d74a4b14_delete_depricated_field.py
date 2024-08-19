"""Delete depricated field

Revision ID: 37c3d74a4b14
Revises: 908b6f8e61ac
Create Date: 2024-08-19 14:27:24.217236

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '37c3d74a4b14'
down_revision: Union[str, None] = '908b6f8e61ac'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column("processed_storage", "filename")


def downgrade() -> None:
    op.add_column('processed_storage', sa.Column('filename', sa.String(), nullable=False))
