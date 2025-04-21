"""Create comics table

Revision ID: 68d246113159
Revises: 9925d121ce6b
Create Date: 2025-04-21 15:05:42.893022

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '68d246113159'
down_revision: Union[str, None] = '9925d121ce6b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("comics",
                    sa.Column("id", sa.Integer, primary_key=True),
                    sa.Column("title", sa.String(50), nullable=False),
                    sa.Column("author", sa.String(50), nullable=False),
                    sa.Column("genre", sa.String(50), nullable=False),
                    sa.Column("published_date", sa.String(10), nullable=False),
                    sa.Column("rating", sa.Integer, nullable=True),
                    sa.Column("user_id", sa.Integer, sa.ForeignKey('users.id'), nullable=False),
                    sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
                    sa.UniqueConstraint("title", name="uq_comic_title")
                    )

def downgrade() -> None:
    op.drop_table("comics")