"""create user table

Revision ID: 1cbf7a0de2d9
Revises: 
Create Date: 2024-06-04 11:55:02.478359

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '1cbf7a0de2d9'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("users",
                    sa.Column("id", sa.Integer, nullable=False, primary_key=True),
                    sa.Column("firstname", sa.String, nullable=False),
                    sa.Column("lastname", sa.String, nullable=False),
                    sa.Column("username", sa.String, nullable=False, unique=True),
                    sa.Column("email", sa.String, nullable=False, unique=True),
                    sa.Column("password", sa.String, nullable=False),
                    sa.Column("registered_at", sa.TIMESTAMP(timezone=True), server_default=sa.func.now()))


def downgrade() -> None:
    op.drop_table("users")
