from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class EntityType(Base):
    __tablename__ = "entity_types"

    entity_type: Mapped[str] = mapped_column(primary_key=True)
