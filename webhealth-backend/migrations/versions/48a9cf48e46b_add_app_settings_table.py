"""add app settings table

Revision ID: 48a9cf48e46b
Revises: 2615aa8a367a
Create Date: 2025-11-23 20:20:03.492310

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '48a9cf48e46b'
down_revision: Union[str, Sequence[str], None] = '2615aa8a367a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "app_settings",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email_notifications", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("slack_notifications", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("push_notifications", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("webhook_url", sa.String(length=2048)),
        sa.Column("email_address", sa.String(length=255)),
        sa.Column("check_interval", sa.Integer(), nullable=False, server_default="60"),
        sa.Column("retry_attempts", sa.Integer(), nullable=False, server_default="3"),
        sa.Column("timeout_seconds", sa.Integer(), nullable=False, server_default="30"),
        sa.Column("ssl_verification", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("follow_redirects", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_table("app_settings")
