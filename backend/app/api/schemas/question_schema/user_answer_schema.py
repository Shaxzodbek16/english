from pydantic import BaseModel, Field, model_validator, ConfigDict
from fastapi import HTTPException, status
from datetime import date, datetime


class UserAnswerBase(BaseModel):
    question_id: int | None = None
    option_id: int | None = None

    model_config = ConfigDict(from_attributes=True)


class UserAnswerCreateSchema(UserAnswerBase):
    @model_validator(mode="after")
    def validate_fields(self):
        if self.question_id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Question ID must be provided",
            )
        if self.option_id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Option ID must be provided",
            )
        return self


class UserAnswerResponseSchema(UserAnswerBase):
    id: int
    created_at: datetime
    updated_at: datetime | None = None


class UserAnswerQuery(BaseModel):
    start_date: date | None = Field(
        default=date.today(), description="Default to 2024-01-01"
    )
    end_date: date | None = Field(
        default=date.today(), description="Default to 2024-01-01"
    )
    page: int = Field(
        default=1, ge=1, description="Page number for pagination, starting from 1"
    )
    size: int = Field(
        default=10, ge=1, le=100, description="Number of items per page, max 100"
    )

    @model_validator(mode="after")
    def validate_page_and_size(self):
        if self.page < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Page number must be greater than or equal to 1",
            )
        if self.size < 1 or self.size > 100:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Size must be between 1 and 100",
            )
        return self

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.size

    @property
    def limit(self) -> int:
        return self.size

    model_config = ConfigDict(from_attributes=True)


class UserAnswerListResponseSchema(UserAnswerQuery):
    total: int = Field(default=0, description="Total number of user answers")
    correct_answers: int = Field(default=0, description="Number of correct answers")
    total_questions: int = Field(
        default=0, description="Total number of questions answered"
    )
    accuracy: float = Field(default=0.0, description="Accuracy of the user's answers")
    user_answers: list[UserAnswerResponseSchema] = Field(
        default_factory=list, description="List of user answers"
    )

    @model_validator(mode="after")
    def calculate_accuracy(self):
        if self.total_questions > 0:
            self.accuracy = (self.correct_answers / self.total_questions) * 100
        else:
            self.accuracy = 0.0
        return self

    model_config = ConfigDict(from_attributes=True)
