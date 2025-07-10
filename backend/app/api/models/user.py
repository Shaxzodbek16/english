from __future__ import annotations
from sqlalchemy import String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, UTC

from app.core.models.base import TimestampMixin
from app.core.settings import get_settings, Settings


class User(TimestampMixin):
    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True, unique=True)
    language: Mapped[str] = mapped_column(String(2), nullable=False, default="en", index=True)
    phone_number: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True)
    profile_picture: Mapped[str | None] = mapped_column(String(255), nullable=True, default=None)
    is_admin: Mapped[bool] = mapped_column(default=False, nullable=False, index=True)

    def update(self, data: dict) -> "User":
        for key, value in data.items():
            if hasattr(self, key):
                if value is not None:
                    setattr(self, key, value)
        setattr(self, "updated_at", datetime.now(UTC))
        return self

    def __repr__(self) -> str:
        return f"<User(id={self.id}, first_name='{self.first_name}', last_name='{self.last_name}', telegram_id={self.telegram_id})>"

    def __str__(self) -> str:
        return self.__repr__()
