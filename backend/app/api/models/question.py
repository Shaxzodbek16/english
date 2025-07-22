from __future__ import annotations
from sqlalchemy import String, TEXT, Boolean, Integer, BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.schema import UniqueConstraint
from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime, UTC,date
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.api.models import User, Level

from app.core.models.base import TimestampMixin


class Question(TimestampMixin):
    __tablename__ = "questions"

    name: Mapped[str] = mapped_column(
        String(255), nullable=False, index=True, unique=True
    )
    picture: Mapped[str | None] = mapped_column(String(255), nullable=True)
    answer: Mapped[str | None] = mapped_column(TEXT, nullable=True, default=None)
    type: Mapped[str] = mapped_column(
        String(50), nullable=False, default="question", index=True
    )  # note: there is also a "daily" type for this field

    # foreign keys
    level_id: Mapped[int] = mapped_column(
        ForeignKey("levels.id"), nullable=False, index=True
    )
    theme_id: Mapped[int] = mapped_column(
        ForeignKey("levels.id"), nullable=False, index=True
    )

    # relationships
    level: Mapped["Level"] = relationship(
        "Level", back_populates="level_questions", foreign_keys=[level_id]
    )
    theme: Mapped["Level"] = relationship(
        "Level", back_populates="theme_questions", foreign_keys=[theme_id]
    )
    options: Mapped[list["Option"]] = relationship(
        "Option", back_populates="question", cascade="all, delete-orphan"
    )
    user_answers: Mapped[list["UserAnswer"]] = relationship(
        "UserAnswer", back_populates="question", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Question(id={self.id}, name='{self.name}', picture='{self.picture}')>"

    def __str__(self):
        return f"Question(name='{self.name}', picture='{self.picture}', answer='{self.answer}')"

    def update(self, data: dict) -> "Question":
        for key, value in data.items():
            if hasattr(self, key):
                if value is not None:
                    setattr(self, key, value)
        setattr(self, "updated_at", datetime.now(UTC))
        return self


class Option(TimestampMixin):
    __tablename__ = "options"
    __table_args__ = (
        UniqueConstraint("question_id", "option", name="uq_question_option"),
    )
    question_id: Mapped[int] = mapped_column(
        ForeignKey("questions.id"), nullable=False, index=True
    )
    option: Mapped[str] = mapped_column(String(255), nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # relationships
    question: Mapped[Question] = relationship("Question", back_populates="options")

    def __repr__(self):
        return f"<Option(question_id={self.question_id}, option_text='{self.option}', is_correct={self.is_correct})>"

    def __str__(self):
        return f"Option(question_id={self.question_id}, option_text='{self.option}', is_correct={self.is_correct})"

    def update(self, data: dict) -> "Option":
        for key, value in data.items():
            if hasattr(self, key):
                if value is not None:
                    setattr(self, key, value)
        setattr(self, "updated_at", datetime.now(UTC))
        return self


class UserAnswer(TimestampMixin):
    __tablename__ = "user_answers"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False, index=True
    )
    question_id: Mapped[int] = mapped_column(
        ForeignKey("questions.id"), nullable=False, index=True
    )
    option_id: Mapped[int] = mapped_column(
        ForeignKey("options.id"), nullable=False, index=True
    )

    # relationships
    question: Mapped[Question] = relationship("Question", back_populates="user_answers")
    option: Mapped[Option] = relationship("Option")
    user: Mapped[User] = relationship("User", back_populates="answers")

    def __repr__(self):
        return f"<UserAnswer(user_id={self.user_id}, question_id={self.question_id}, option_id={self.option_id})>"

    def __str__(self):
        return f"UserAnswer(user_id={self.user_id}, question_id={self.question_id}, option_id={self.option_id})"

    def update(self, data: dict) -> "UserAnswer":
        for key, value in data.items():
            if hasattr(self, key):
                if value is not None:
                    setattr(self, key, value)
        setattr(self, "updated_at", datetime.now(UTC))
        return self



class UserQuestionResult(TimestampMixin):
    __tablename__ = "user_quiz_results"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False, index=True
    )
    question_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True)
    score: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    questions: Mapped[list] = mapped_column(JSON, nullable=False, default=[])

    # relationships
    user: Mapped[User] = relationship("User", back_populates="results")

    def __repr__(self):
        return f"<UserQuizResult(user_id={self.user_id}, question_id={self.question_id}, score={self.score})>"

    def __str__(self):
        return f"UserQuizResult(user_id={self.user_id}, question_id={self.question_id}, score={self.score})"

    def update(self, data: dict) -> "UserQuizResult":
        for key, value in data.items():
            if hasattr(self, key):
                if value is not None:
                    setattr(self, key, value)
        setattr(self, "updated_at", datetime.now(UTC))
        return self

    def get_created_date(self)->date:
        return self.created_at.date()
