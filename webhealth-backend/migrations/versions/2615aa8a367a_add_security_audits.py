"""add security audits

Revision ID: 2615aa8a367a
Revises: 
Create Date: 2025-11-23 17:26:31.777960

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "2615aa8a367a"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


security_status_enum = sa.Enum(
    "pass",
    "warning",
    "critical",
    name="securityauditstatus",
)


def upgrade() -> None:
    op.add_column(
        "monitors",
        sa.Column(
            "last_security_check_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
    )
    op.add_column(
        "monitors",
        sa.Column(
            "security_status",
            security_status_enum,
            nullable=False,
            server_default="pass",
        ),
    )

    op.create_table(
        "security_audits",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "monitor_id",
            sa.Integer(),
            sa.ForeignKey("monitors.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("status", security_status_enum, nullable=False),
        sa.Column("findings", sa.JSON(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_table("security_audits")
    op.drop_column("monitors", "security_status")
    op.drop_column("monitors", "last_security_check_at")
    security_status_enum.drop(op.get_bind(), checkfirst=False)
