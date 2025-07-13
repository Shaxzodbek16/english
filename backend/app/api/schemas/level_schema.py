from datetime import datetime
from fastapi import HTTPException, status

from pydantic import BaseModel, Field, ConfigDict, model_validator

from app.api.schemas import PaginationSchema, QueryParamsSchema


class LevelBase(BaseModel):
    name: str | None = None
    description: str | None = None
    picture: str | None = None
    type: str | None = None

    model_config = ConfigDict(from_attributes=True)


class LevelCreateSchema(LevelBase):
    @model_validator(mode="after")
    def validate_data(self) -> "LevelCreateSchema":
        if not self.name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Name cannot be empty."
            )
        if not isinstance(self.name, str):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Name must be a string."
            )
        if self.description and not isinstance(self.description, str):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Description must be a string if provided.",
            )
        if self.type and self.type not in ["level", "theme", "section"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid type. Valid types are: {' ,'.join(['level', 'theme', 'section'])}.",
            )
        return self

    model_config = ConfigDict(from_attributes=True, extra="forbid")


class LevelUpdateSchema(LevelBase):
    @model_validator(mode="after")
    def validate_update_data(self) -> "LevelUpdateSchema":
        if self.type and self.type not in ["level", "theme", "section"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid type. Valid types are: {' ,'.join(['level', 'theme', 'section'])}.",
            )
        if not any([self.name, self.description, self.picture, self.type]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least one field must be provided for update.",
            )
        return self

    model_config = ConfigDict(from_attributes=True, extra="forbid")


class LevelResponseSchema(LevelBase):
    id: int
    created_at: datetime
    updated_at: datetime | None = None


class LevelListResponseSchema(PaginationSchema):
    items: list[LevelResponseSchema] = Field(default_factory=list)
    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="after")
    def validate_filter_or_sort(self) -> "LevelListResponseSchema":
        if self.filter:
            valid_filters = ["name", "description", "picture"]
            if not self.filter.lstrip("-") in valid_filters:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid filter field. Valid filters are: {', '.join(valid_filters)}",
                )
        if self.sort:
            valid_sorts = [
                "id",
                "name",
                "description",
                "picture",
                "created_at",
                "updated_at",
            ]
            if not self.sort.lstrip("-") in valid_sorts:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid sort field. Valid sorts are: {', '.join(valid_sorts)}",
                )
        return self


class LevelQueryParamsSchema(QueryParamsSchema):
    type: str | None = None

    @model_validator(mode="after")
    def validate_type(self) -> "LevelQueryParamsSchema":
        if self.type and self.type not in ["level", "theme", "section"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid type. Valid types are: {' ,'.join(['level', 'theme', 'section'])}.",
            )
        return self
