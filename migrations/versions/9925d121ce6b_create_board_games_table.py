"""Create board_games table

Revision ID: 9925d121ce6b
Revises: 4b4c1cd615c0
Create Date: 2025-04-21 15:05:29.167965

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9925d121ce6b'
down_revision: Union[str, None] = '4b4c1cd615c0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("board_games",
                    sa.Column("id", sa.Integer, primary_key=True),
                    sa.Column("title", sa.String(50), nullable=False),
                    sa.Column("designer", sa.String(50), nullable=False),
                    sa.Column("genre", sa.String(50), nullable=False),
                    sa.Column("release_date", sa.String(10), nullable=False),
                    sa.Column("rating", sa.Integer, nullable=True),
                    sa.Column("user_id", sa.Integer, sa.ForeignKey('users.id'), nullable=False),
                    sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
                    sa.UniqueConstraint("title", name="uq_game_title")
                    )

def downgrade() -> None:
    op.drop_table("board_games")