"""create users

Revision ID: 0001
Revises:
Create Date: 2026-07-13 12:37:05.213581

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0001"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    # Seed the mandatory V1 bootstrap user in the same migration, so a
    # fresh install is fully initialized after `alembic upgrade head`
    # alone — no separate seed command. A self-contained table() /
    # column() construct is used deliberately instead of importing the
    # live ORM model, per Alembic's own documented recommendation: this
    # migration must remain stable even if the User model changes later
    # (id and created_at are left to their server_default above).
    users_table = sa.table("users", sa.column("email", sa.String))
    op.bulk_insert(users_table, [{"email": "admin@lifeos.local"}])


def downgrade() -> None:
    op.drop_table("users")
