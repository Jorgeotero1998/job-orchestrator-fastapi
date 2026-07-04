"""jobs tables

Revision ID: 0002_jobs_tables
Revises: 0001_init_users
Create Date: 2026-07-04
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "0002_jobs_tables"
down_revision = "0001_init_users"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "jobs_definitions",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("description", sa.String(length=300), nullable=False, server_default=""),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )
    op.create_index("ux_jobs_definitions_name", "jobs_definitions", ["name"], unique=True)

    op.create_table(
        "jobs_runs",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column(
            "job_id",
            sa.dialects.postgresql.UUID(as_uuid=True),
            sa.ForeignKey("jobs_definitions.id"),
            nullable=False,
        ),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="queued"),
        sa.Column("input_json", sa.Text(), nullable=False, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )
    op.create_index("ix_jobs_runs_job_id", "jobs_runs", ["job_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_jobs_runs_job_id", table_name="jobs_runs")
    op.drop_table("jobs_runs")
    op.drop_index("ux_jobs_definitions_name", table_name="jobs_definitions")
    op.drop_table("jobs_definitions")

