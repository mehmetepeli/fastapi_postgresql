"""Create user table

Revision ID: aa2699453ea4
Revises: 
Create Date: 2025-04-21 15:04:38.422914

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aa2699453ea4'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("users",
                    sa.Column("id", sa.Integer, primary_key=True),
                    sa.Column("name", sa.String(50), nullable=False),
                    sa.Column("username", sa.String(50), nullable=False),
                    sa.Column("email", sa.String(100), nullable=False),
                    sa.Column("password", sa.String(100), nullable=False),
                    sa.Column("role", sa.String(10), nullable=True, default="user"),
                    sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
                    sa.UniqueConstraint("username", name="uq_username"),
                    )

def downgrade() -> None:
    op.drop_table("users")