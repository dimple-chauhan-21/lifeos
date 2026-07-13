import uuid
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, func, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class EntityType(Base):
    __tablename__ = "entity_types"

    entity_type: Mapped[str] = mapped_column(primary_key=True)


class Entity(Base):
    __tablename__ = "entities"
    __table_args__ = (
        CheckConstraint(
            "lifecycle_state IN ('active', 'archived', 'trashed')",
            name="ck_entities_lifecycle_state",
        ),
        Index(
            "ix_entities_owner_id_entity_type_lifecycle_state",
            "owner_id",
            "entity_type",
            "lifecycle_state",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    entity_type: Mapped[str] = mapped_column(ForeignKey("entity_types.entity_type"), nullable=False)
    owner_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    name: Mapped[str] = mapped_column(nullable=False)
    is_favorite: Mapped[bool] = mapped_column(nullable=False, server_default=text("false"))
    lifecycle_state: Mapped[str] = mapped_column(nullable=False, server_default=text("'active'"))
    trashed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("now()"),
        onupdate=func.now(),
    )
