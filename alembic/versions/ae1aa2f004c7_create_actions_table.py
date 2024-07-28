"""create actions table

Revision ID: ae1aa2f004c7
Revises: d37c231cdc3d
Create Date: 2024-07-28 12:50:44.267403

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM

# revision identifiers, used by Alembic.
revision: str = 'ae1aa2f004c7'
down_revision: Union[str, None] = 'd37c231cdc3d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("actions",
                    sa.Column("action_id", sa.Integer, nullable=False, primary_key=True, autoincrement=True),
                    sa.Column("raw_file_uuid", sa.UUID(as_uuid=True),
                              sa.ForeignKey("raw_storage.file_uuid"),
                              nullable=False, unique=True),
                    sa.Column("processed_file_uuid", sa.UUID(as_uuid=True),
                              sa.ForeignKey("processed_storage.file_uuid"),
                              nullable=False, unique=True),
                    sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False),
                    sa.Column("service_type", ENUM(name="servicetype", create_type=False)),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.func.now()))


def downgrade() -> None:
    op.drop_table("actions")
