"""Add achievements to table

Revision ID: 908b6f8e61ac
Revises: 4600e362f62a
Create Date: 2024-08-02 15:51:13.618936

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from database.database_types import ServiceType

# revision identifiers, used by Alembic.
revision: str = '908b6f8e61ac'
down_revision: Union[str, None] = '4600e362f62a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()

    achievement_list = [
        # Video achievements
        {"name": "Music Lover", "description": "Perform 3 conversions from mp4 to mp3", "service": ServiceType.video,
         "image_name": "ada1.png"},
        {"name": "Video Editor", "description": "Edit 5 video files", "service": ServiceType.video,
         "image_name": "ada2.png"},
        {"name": "Director", "description": "Create a movie with at least 10 scenes", "service": ServiceType.video,
         "image_name": "ada3.png"},

        # image_name achievements
        {"name": "Photographer", "description": "Upload 10 images", "service": ServiceType.image,
         "image_name": "leon1.png"},
        {"name": "Image Enhancer", "description": "Enhance the quality of 5 images", "service": ServiceType.image,
         "image_name": "leon2.png"},
        {"name": "Collage Creator", "description": "Create 3 image_name collages", "service": ServiceType.image,
         "image_name": "leon3.png"},

        # Audio achievements
        {"name": "Audiophile", "description": "Upload 20 audio files", "service": ServiceType.audio,
         "image_name": "ashley1.png"},
        {"name": "Audio Mixer", "description": "Mix 5 audio tracks", "service": ServiceType.audio,
         "image_name": "ashley2.png"},
        {"name": "Podcast Creator", "description": "Create a podcast episode", "service": ServiceType.audio,
         "image_name": "ashley3.png"}
    ]

    conn.execute(
        sa.text(
            "INSERT INTO achievements (name, description, service, image_name) VALUES (:name, :description, :service, :image_name)"),
        achievement_list
    )


def downgrade() -> None:
    op.execute("DELETE FROM user_achievements")
    op.execute("DELETE FROM achievements")
