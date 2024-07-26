"""Create Storage table

Revision ID: 0b7d86243c6b
Revises: 1cbf7a0de2d9
Create Date: 2024-07-26 20:24:29.944820

"""
from typing import Sequence, Union
from uuid import uuid4

from alembic import op
import sqlalchemy as sa
from database.database_types import FileState, ServiceType, FileExtension

# revision identifiers, used by Alembic.
revision: str = '0b7d86243c6b'
down_revision: Union[str, None] = '1cbf7a0de2d9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("storage",
                    sa.Column("file_id", sa.Integer, nullable=False, primary_key=True, autoincrement=True),
                    sa.Column("file_uuid", sa.UUID(as_uuid=True), nullable=False, unique=True),
                    sa.Column("filename", sa.String, nullable=False),
                    sa.Column("file_extension", sa.Enum(FileExtension), nullable=False),
                    sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False),
                    sa.Column("file_state", sa.Enum(FileState), nullable=False),
                    sa.Column("service_type", sa.Enum(ServiceType), nullable=False),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.func.now()))


def downgrade() -> None:
    op.drop_table("storage")
    op.execute("DROP TYPE filestate")
    op.execute("DROP TYPE servicetype")
