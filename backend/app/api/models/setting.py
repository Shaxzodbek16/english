from fastapi import HTTPException, status
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.api.models.user import User

from app.core.models.base import BaseModel


class Setting(BaseModel):
    __tablename__ = "setting"

    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # relationships
    user: Mapped["User"] = relationship(back_populates="settings")

    settings: Mapped[dict] = mapped_column(JSONB, default={}, nullable=False)

    def __repr__(self):
        return f"<Setting(id={self.id}, settings={self.settings})>"

    def __str__(self):
        return f"Setting(id={self.id}, settings={self.settings})"

    def update(self, data: dict) -> "Setting":
        if not isinstance(data, dict):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Settings must be a dictionary.",
            )
        if data is None or not data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Settings cannot be empty.",
            )
        setattr(self, "settings", data)
        return self
