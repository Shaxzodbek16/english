from sqlalchemy.orm import declarative_base
from datetime import datetime, UTC
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.orm import Mapped

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True
    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True, index=True)


class TimestampMixin(BaseModel):
    __abstract__ = True
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.now(UTC), nullable=False)
    updated_at: Mapped[datetime] = Column(DateTime, onupdate=datetime.now(UTC), nullable=True)
