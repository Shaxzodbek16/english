from __future__ import annotations
from sqlalchemy import String, BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, UTC

from app.core.models.base import TimestampMixin


class Entertainment(TimestampMixin):
    __tablename__ = "entertainments"

    message_id: Mapped[int] = mapped_column(BigInteger, index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(255), index=True, nullable=False)

    type_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("entertainment_types.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    type: Mapped["EntertainmentTypes"] = relationship(back_populates="entertainments")

    def __repr__(self):
        return f"<Entertainment(id={self.id}, title='{self.title}', type_id={self.type_id})>"

    def __str__(self):
        return (
            f"Entertainment(id={self.id}, title='{self.title}', type_id={self.type_id})"
        )

    def update(self, data: dict) -> "Entertainment":
        for key, value in data.items():
            if hasattr(self, key) and value is not None:
                setattr(self, key, value)
        self.updated_at = datetime.now(UTC)
        return self


class EntertainmentTypes(TimestampMixin):
    __tablename__ = "entertainment_types"

    name: Mapped[str] = mapped_column(
        String(50), index=True, nullable=False, unique=True
    )

    entertainments: Mapped[list["Entertainment"]] = relationship(
        back_populates="type", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<EntertainmentTypes(name={self.name})>"

    def __str__(self):
        return f"EntertainmentTypes(name='{self.name}')"

    def update(self, data: dict) -> "EntertainmentTypes":
        for key, value in data.items():
            if hasattr(self, key) and value is not None:
                setattr(self, key, value)
        self.updated_at = datetime.now(UTC)
        return self
