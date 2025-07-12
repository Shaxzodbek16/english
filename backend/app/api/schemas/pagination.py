from __future__ import annotations
from pydantic import BaseModel, Field, ConfigDict, model_validator
from typing import Any
from fastapi import HTTPException, status


class PaginationSchema(BaseModel):
    page: int = Field(default=1, ge=1)
    size: int = Field(default=10, ge=1, le=100)
    search: str | None = None
    sort: str | None = None
    filter: str | None = None
    total: int = 0
    items: list[Any] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.size

    @property
    def limit(self) -> int:
        return self.size


class QueryParamsSchema(BaseModel):
    page: int = 1
    size: int = 10
    search: str | None = None
    filter: str | None = None
    sort: str | None = None

    model_config = ConfigDict(from_attributes=True)

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.size

    @property
    def limit(self) -> int:
        return self.size

    @model_validator(mode="after")
    def validate_and_clamp(self) -> "QueryParamsSchema":
        if self.page < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Page number must be greater than or equal to 1.",
            )
        if self.size > 100 or self.size < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Page size must be greater than 0 and less than or equal to 100.",
            )
        return self
