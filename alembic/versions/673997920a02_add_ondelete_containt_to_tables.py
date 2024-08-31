"""Add ONDELETE containt to tables

Revision ID: 673997920a02
Revises: 37c3d74a4b14
Create Date: 2024-08-29 19:38:44.620191

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '673997920a02'
down_revision: Union[str, None] = '37c3d74a4b14'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

table_names = ("actions", "user_achievements", "raw_storage", "processed_storage")


def upgrade() -> None:
    for tablename in table_names:
        constraint_field = f"{tablename}_user_id_fkey"
        op.drop_constraint(constraint_field, tablename, type_="foreignkey")
        op.create_foreign_key(constraint_field, tablename, "users", ["user_id"], ["id"], ondelete="CASCADE")


def downgrade() -> None:
    for tablename in table_names:
        constraint_field = f"{tablename}_user_id_fkey"
        op.drop_constraint(constraint_field, tablename, type_="foreignkey")
        op.create_foreign_key(constraint_field, tablename, "users", ["user_id"], ["id"])
