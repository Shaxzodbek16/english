from pydantic import BaseModel, Field, ConfigDict, model_validator
from datetime import datetime
from fastapi import HTTPException, status

from app.api.schemas.pagination import PaginationSchema, QueryParamsSchema
from app.api.schemas.question_schema.option_schema import OptionResponseSchema


class QuestionBase(BaseModel):
    name: str | None = None
    picture: str | None = None
    answer: str | None = None
    type: str | None = "question"
    level_id: int | None = None
    theme_id: int | None = None
    model_config = ConfigDict(from_attributes=True)


class QuestionCreateSchema(QuestionBase):
    @model_validator(mode="after")
    def validate_fields(
        self,
    ):
        if self.name is None or self.name.strip() == "":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Name must be provided and cannot be empty.",
            )
        if self.level_id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Level ID must be provided",
            )
        if self.theme_id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Theme ID must be provided",
            )
        if self.type not in [
            "question",
            "daily",
        ]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Type must be either 'question' or 'daily'.",
            )
        return self


class QuestionUpdateSchema(QuestionBase):
    @model_validator(mode="after")
    def validate_fields(self):
        if not any(
            [
                self.name,
                self.picture,
                self.answer,
                self.type,
                self.level_id,
                self.theme_id,
            ]
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least one field must be provided for update.",
            )
        return self


class QuestionResponseSchema(QuestionBase):
    id: int
    variants: list[OptionResponseSchema] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime | None = None


class QuestionListResponseSchema(PaginationSchema):
    items: list[QuestionResponseSchema] = Field(
        default_factory=list,
        description="List of questions.",
    )


class QuestionQueryParamSchema(QueryParamsSchema):
    level_id: int | None = None
    theme_id: int | None = None

    @model_validator(mode="after")
    def validate_fields(self) -> "QuestionQueryParamSchema":
        if self.level_id is not None and self.level_id < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Level ID must be greater than or equal to 1.",
            )
        if self.theme_id is not None and self.theme_id < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Theme ID must be greater than or equal to 1.",
            )
        return self
