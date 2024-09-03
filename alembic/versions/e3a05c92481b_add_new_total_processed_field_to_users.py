"""add new total_processed field to users

Revision ID: e3a05c92481b
Revises: 9b9f21ed4232
Create Date: 2024-09-03 16:27:46.921534

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'e3a05c92481b'
down_revision: Union[str, None] = '9b9f21ed4232'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("total_processed", sa.Integer, server_default=sa.text("0")))


def downgrade() -> None:
    op.drop_column("users", "total_processed")
