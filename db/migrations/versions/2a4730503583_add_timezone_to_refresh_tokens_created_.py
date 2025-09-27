"""Add timezone to refresh_tokens.created_at

Revision ID: 2a4730503583
Revises: 9e142dc30bdb
Create Date: 2025-09-27 04:16:15.855695

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2a4730503583'
down_revision: Union[str, None] = '9e142dc30bdb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "refresh_tokens",
        "created_at",
        server_default=sa.func.now(),
        existing_type=sa.DateTime(timezone=True),
    )


def downgrade() -> None:
    op.alter_column(
        "refresh_tokens",
        "created_at",
        server_default=None,
        existing_type=sa.DateTime(timezone=True),
    )
