"""create user_achievement table

Revision ID: 4600e362f62a
Revises: 6f5b046ec9b5
Create Date: 2024-08-02 15:40:31.243528

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '4600e362f62a'
down_revision: Union[str, None] = '6f5b046ec9b5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("user_achievements",
                    sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False),
                    sa.Column("achievement_name", sa.String, sa.ForeignKey("achievements.name"), nullable=False),
                    sa.PrimaryKeyConstraint("user_id", "achievement_name", name="user_achievement_pk")
                    )


def downgrade() -> None:
    op.drop_table("user_achievements")
