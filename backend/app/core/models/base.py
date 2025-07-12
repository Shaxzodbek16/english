from sqlalchemy.orm import declarative_base, mapped_column
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, func
from sqlalchemy.orm import Mapped

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True
    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True, index=True)


class TimestampMixin(BaseModel):
    __abstract__ = True
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
