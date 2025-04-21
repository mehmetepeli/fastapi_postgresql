"""Create books table

Revision ID: 7ce2b7b00b9b
Revises: aa2699453ea4
Create Date: 2025-04-21 15:05:08.897113

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7ce2b7b00b9b'
down_revision: Union[str, None] = 'aa2699453ea4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("books",
                    sa.Column("id", sa.Integer, primary_key=True),
                    sa.Column("title", sa.String(50), nullable=False),
                    sa.Column("author", sa.String(50), nullable=False),
                    sa.Column("genre", sa.String(50), nullable=False),
                    sa.Column("published_date", sa.String(10), nullable=False),
                    sa.Column("rating", sa.Integer, nullable=True),
                    sa.Column("user_id", sa.Integer, sa.ForeignKey('users.id'), nullable=False),
                    sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
                    sa.UniqueConstraint("title", name="uq_book_title"),
                    )

def downgrade() -> None:
    op.drop_table("books")