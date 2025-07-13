from __future__ import annotations
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, UTC

from app.core.models.base import TimestampMixin


class Level(TimestampMixin):
    __tablename__ = "levels"
    name: Mapped[str] = mapped_column(
        String(255), index=True, nullable=False, unique=True
    )
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    picture: Mapped[str | None] = mapped_column(
        String(255), nullable=True, default=None
    )
    type: Mapped[str] = mapped_column(
        String(50), nullable=False, default="level", index=True
    )

    def __repr__(self):
        return f"<Level(id={self.id}, name='{self.name}', description='{self.description}')>"

    def __str__(self):
        return f"Level(name='{self.name}', description='{self.description}', picture='{self.picture}')"

    def update(self, data: dict) -> Level:
        for key, value in data.items():
            if hasattr(self, key):
                if value is not None:
                    setattr(self, key, value)
        setattr(self, "updated_at", datetime.now(UTC))
        return self
