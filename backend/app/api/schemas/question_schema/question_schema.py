from pydantic import BaseModel, Field, ConfigDict, model_validator
from datetime import datetime

from .pagination import QueryParamsSchema, PaginationSchema


class QuestionBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class QuestionCreateSchema(QuestionBase):
    pass


class QuestionUpdateSchema(QuestionBase):
    pass


class QuestionResponseSchema(QuestionBase):
    id: int
    created_at: datetime
    updated_at: datetime | None = None


class QuestionListResponseSchema(PaginationSchema):
    items: list[QuestionResponseSchema] = Field(
        default_factory=list, description="List of questions."
    )
