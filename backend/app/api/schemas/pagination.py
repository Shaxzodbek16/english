from pydantic import BaseModel, Field, ConfigDict
from typing import Any


class PaginationSchema(BaseModel):
    page: int = 1
    size: int = 10
    search: str | None = None
    sort: str | None = None
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
    sort: str | None = None

    model_config = ConfigDict(from_attributes=True)

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.size

    @property
    def limit(self) -> int:
        return self.size
