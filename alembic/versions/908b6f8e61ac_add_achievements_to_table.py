"""Add achievements to table

Revision ID: 908b6f8e61ac
Revises: 4600e362f62a
Create Date: 2024-08-02 15:51:13.618936

"""
from typing import Sequence, Union

from alembic import op
from data import achievement_list_old
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '908b6f8e61ac'
down_revision: Union[str, None] = '4600e362f62a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()

    conn.execute(
        sa.text(
            "INSERT INTO achievements (name, description, service, image_name) VALUES (:name, :description, :service, :image_name)"),
        achievement_list_old
    )


def downgrade() -> None:
    op.execute("DELETE FROM user_achievements")
    op.execute("DELETE FROM achievements")
