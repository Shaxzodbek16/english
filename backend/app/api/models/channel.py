from __future__ import annotations
from sqlalchemy import String, Boolean, BigInteger, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, UTC

from app.core.models.base import TimestampMixin


class Channel(TimestampMixin):
    __tablename__ = "channels"

    name: Mapped[str] = mapped_column(String, index=True, nullable=False)
    link: Mapped[str] = mapped_column(String, index=True, nullable=False)
    channel_id: Mapped[int] = mapped_column(
        BigInteger, unique=True, index=True, nullable=False
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False, index=True
    )
    till: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        default=func.now(),
        index=True,
    )

    def __repr__(self):
        return f"<Channel(id={self.id}, name='{self.name}', link='{self.link}')>"

    def __str__(self):
        return f"Channel(name='{self.name}', link='{self.link}', channel_id={self.channel_id}, is_active={self.is_active}, till={self.till})"

    def is_expired(self):
        if self.till is None:
            return False
        return self.till < datetime.utcnow() and self.is_active

    def update(self, data: dict):
        for key, value in data.items():
            if hasattr(self, key):
                if value is not None:
                    setattr(self, key, value)
        setattr(self, "updated_at", datetime.utcnow())
        return self
