"""create achievement table

Revision ID: 6f5b046ec9b5
Revises: ae1aa2f004c7
Create Date: 2024-08-02 15:34:44.504065

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from database.database_types import ServiceType
from sqlalchemy.dialects.postgresql import ENUM

# revision identifiers, used by Alembic.
revision: str = '6f5b046ec9b5'
down_revision: Union[str, None] = 'ae1aa2f004c7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("achievements",
                    sa.Column("name", sa.String, primary_key=True, nullable=False, unique=True),
                    sa.Column("description", sa.String, nullable=False),
                    sa.Column("service", ENUM(name="servicetype", create_type=False), nullable=False),
                    sa.Column("image_name", sa.String, nullable=False)
                    )


def downgrade() -> None:
    op.drop_table("achievements")
