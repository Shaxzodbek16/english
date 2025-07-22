from __future__ import annotations
from sqlalchemy import String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, UTC, date
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.api.models import UserAnswer, UserQuizResult, Setting

from app.core.models.base import TimestampMixin
from app.core.settings import get_settings, Settings

settings: Settings = get_settings()


class User(TimestampMixin):
    __tablename__ = "users"

    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    telegram_id: Mapped[int] = mapped_column(
        BigInteger, nullable=False, index=True, unique=True
    )
    language: Mapped[str] = mapped_column(
        String(10), nullable=False, default="en", index=True
    )
    phone_number: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True)
    profile_picture: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_admin: Mapped[bool] = mapped_column(default=False, nullable=False, index=True)

    # relationships
    answers: Mapped[list["UserAnswer"]] = relationship(
        "UserAnswer", back_populates="user", cascade="all, delete-orphan"
    )
    results: Mapped[list["UserQuizResult"]] = relationship(
        "UserQuizResult", back_populates="user", cascade="all, delete-orphan"
    )
    settings: Mapped[list["Setting"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

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

    def to_dict_for_token(self) -> dict:
        return {
            "id": self.id,
            "telegram_id": self.telegram_id,
            "phone_number": self.phone_number,
            "is_admin": self.is_admin,
        }

    @property
    def get_created_time(self) -> date:
        return self.created_at.date()
