"""trigger for completed field

Revision ID: 9b9f21ed4232
Revises: 01ef2eda4712
Create Date: 2024-08-30 17:37:21.632136

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '9b9f21ed4232'
down_revision: Union[str, None] = '01ef2eda4712'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

trigger_func = \
    """
    CREATE OR REPLACE FUNCTION check_completion()
    RETURNS TRIGGER AS $$
    BEGIN
        IF NEW.progress = NEW.target THEN
            NEW.completed := TRUE;
        ELSE
            NEW.completed := FALSE;
        END IF;
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    """

# Создание триггера
trigger = \
    """
    CREATE TRIGGER check_completion_trigger
    BEFORE INSERT OR UPDATE ON user_achievement_progress
    FOR EACH ROW
    EXECUTE FUNCTION check_completion();
    """


def upgrade() -> None:
    # 1.
    op.execute(trigger_func)
    # 2.
    op.execute(trigger)


def downgrade() -> None:
    # 1.
    op.execute("DROP TRIGGER IF EXISTS check_completion_trigger ON user_achievement_progress;")
    # 2.
    op.execute("DROP FUNCTION IF EXISTS check_completion;")
