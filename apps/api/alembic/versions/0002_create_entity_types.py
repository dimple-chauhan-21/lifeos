"""create entity types

Revision ID: 0002
Revises: 0001
Create Date: 2026-07-13 13:10:37.862206

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0002"
down_revision: str | Sequence[str] | None = "0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "entity_types",
        sa.Column("entity_type", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("entity_type"),
    )


def downgrade() -> None:
    op.drop_table("entity_types")
