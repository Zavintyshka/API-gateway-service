"""create processed storage

Revision ID: d37c231cdc3d
Revises: 0b7d86243c6b
Create Date: 2024-07-28 12:10:51.660600

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM

# revision identifiers, used by Alembic.
revision: str = 'd37c231cdc3d'
down_revision: Union[str, None] = '0b7d86243c6b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("processed_storage",
                    sa.Column("file_id", sa.Integer, nullable=False, primary_key=True, autoincrement=True),
                    sa.Column("file_uuid", sa.UUID(as_uuid=True), nullable=False, unique=True),
                    sa.Column("filename", sa.String, nullable=False),
                    sa.Column("file_extension", ENUM(name="fileextension", create_type=False), nullable=False),
                    sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False),
                    sa.Column("service_type", ENUM(name="servicetype", create_type=False)),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.func.now()))


def downgrade() -> None:
    op.drop_table("processed_storage")
