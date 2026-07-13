"""create entities

Revision ID: 0003
Revises: 0002
Create Date: 2026-07-13 13:57:24.315291

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0003"
down_revision: str | Sequence[str] | None = "0002"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "entities",
        sa.Column("id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("entity_type", sa.String(), nullable=False),
        sa.Column("owner_id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("is_favorite", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.Column(
            "lifecycle_state", sa.String(), server_default=sa.text("'active'"), nullable=False
        ),
        sa.Column("trashed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "lifecycle_state IN ('active', 'archived', 'trashed')",
            name="ck_entities_lifecycle_state",
        ),
        sa.ForeignKeyConstraint(["entity_type"], ["entity_types.entity_type"]),
        sa.ForeignKeyConstraint(["owner_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_entities_owner_id_entity_type_lifecycle_state",
        "entities",
        ["owner_id", "entity_type", "lifecycle_state"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_entities_owner_id_entity_type_lifecycle_state", table_name="entities")
    op.drop_table("entities")
