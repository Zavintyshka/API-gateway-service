"""Replace user_achievements table with user_achievement_progres

Revision ID: 356d364d62dd
Revises: 673997920a02
Create Date: 2024-08-30 15:46:51.661668

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '356d364d62dd'
down_revision: Union[str, None] = '673997920a02'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1.
    op.drop_table("user_achievements")

    # 2.
    op.create_table("user_achievement_progress",
                    sa.Column("id", sa.Integer, primary_key=True, nullable=False, autoincrement=True),
                    sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
                    sa.Column("achievement_name", sa.String, sa.ForeignKey("achievements.name"), nullable=False),
                    sa.Column("progress", sa.Integer, server_default=sa.text("0"), nullable=False),
                    sa.Column("target", sa.Integer, nullable=False),
                    sa.Column("completed", sa.Boolean, server_default=sa.text("false"))
                    )


def downgrade() -> None:
    # 1.
    op.create_table("user_achievements",
                    sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False),
                    sa.Column("achievement_name", sa.String, sa.ForeignKey("achievements.name"), nullable=False),
                    sa.PrimaryKeyConstraint("user_id", "achievement_name", name="user_achievement_pk")
                    )

    # 2.
    op.drop_table("user_achievement_progress")
