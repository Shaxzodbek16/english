from pydantic import BaseModel, ConfigDict, Field, model_validator
from fastapi import HTTPException, status
from datetime import datetime

from app.api.schemas.pagination import PaginationSchema


class OptionBase(BaseModel):
    option: str | None = None
    is_correct: bool | None = None
    question_id: int | None = None

    model_config = ConfigDict(from_attributes=True)


class OptionCreateSchema(OptionBase):
    @model_validator(mode="after")
    def validate_fields(self):
        if self.option is None or self.option.strip() == "":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Option cannot be empty for option field",
            )
        if self.question_id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Question ID must be provided",
            )
        if self.is_correct is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="is_correct must be specified",
            )
        return self


class OptionUpdateSchema(OptionBase):
    @model_validator(mode="after")
    def validate_update_fields(self):
        if not any([self.option, self.is_correct, self.question_id]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least one field must be provided for update.",
            )
        return self


class OptionResponseSchema(OptionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    @model_validator(mode="after")
    def validate_response_fields(self):
        if self.id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID must be provided in the response",
            )
        return self


class OptionListResponseSchema(PaginationSchema):
    items: list[OptionResponseSchema] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_filter_or_sort(self) -> "OptionListResponseSchema":
        if self.filter:
            valid_filters = ["is_correct"]
            if not self.filter.lstrip("-") in valid_filters:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid filter field. Valid filters are: {', '.join(valid_filters)}",
                )
        if self.sort:
            valid_sorts = ["id", "created_at", "updated_at"]
            if not self.sort.lstrip("-") in valid_sorts:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid sort field. Valid sorts are: {', '.join(valid_sorts)}",
                )
        return self
