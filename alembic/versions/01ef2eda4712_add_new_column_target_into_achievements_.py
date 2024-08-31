"""add new column Target into achievements table

Revision ID: 01ef2eda4712
Revises: 356d364d62dd
Create Date: 2024-08-30 16:31:02.305733

"""
from typing import Sequence, Union
from data import achievement_list_old, achievement_list_new
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '01ef2eda4712'
down_revision: Union[str, None] = '356d364d62dd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    op.execute(sa.text("DELETE FROM user_achievement_progress"))
    op.execute(sa.text("DELETE FROM achievements"))
    op.add_column("achievements", sa.Column("target", sa.Integer, nullable=False))
    conn.execute(sa.text(
        "INSERT INTO achievements (name, description, service, image_name, target) VALUES (:name, :description, :service, :image_name, :target)"),
        achievement_list_new)


def downgrade() -> None:
    conn = op.get_bind()
    op.execute(sa.text("DELETE FROM user_achievement_progress"))
    op.execute(sa.text("DELETE FROM achievements"))
    op.drop_column("achievements", "target")
    conn.execute(sa.text(
        "INSERT INTO achievements (name, description, service, image_name) VALUES (:name, :description, :service, :image_name)"),
        achievement_list_old)
