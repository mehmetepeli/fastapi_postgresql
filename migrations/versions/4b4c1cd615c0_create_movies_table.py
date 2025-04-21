"""Create movies table

Revision ID: 4b4c1cd615c0
Revises: 7ce2b7b00b9b
Create Date: 2025-04-21 15:05:15.899282

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4b4c1cd615c0'
down_revision: Union[str, None] = '7ce2b7b00b9b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("movies",
                    sa.Column("id", sa.Integer, primary_key=True),
                    sa.Column("title", sa.String(50), nullable=False),
                    sa.Column("director", sa.String(50), nullable=False),
                    sa.Column("genre", sa.String(50), nullable=False),
                    sa.Column("release_date", sa.String(10), nullable=False),
                    sa.Column("rating", sa.Integer, nullable=True),
                    sa.Column("user_id", sa.Integer, sa.ForeignKey('users.id'), nullable=False),
                    sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
                    sa.UniqueConstraint("title", name="uq_movie_title")
                    )

def downgrade() -> None:
    op.drop_table("movies")
