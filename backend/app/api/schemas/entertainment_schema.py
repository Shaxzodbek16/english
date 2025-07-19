from pydantic import BaseModel, ConfigDict, model_validator, Field
from datetime import datetime
from fastapi import HTTPException, status

from app.api.schemas.pagination import PaginationSchema, QueryParamsSchema


class EntertainmentBase(BaseModel):
    title: str | None = None
    type_id: int | None = None

    model_config = ConfigDict(from_attributes=True)


class EntertainmentUpdate(EntertainmentBase):
    title: str | None = None
    type_id: int | None = None

    @model_validator(mode="after")
    def validate_fields(self) -> "EntertainmentUpdate":
        if not any([self.title, self.type_id]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least one field (title or type_id) must be provided.",
            )
        if self.type_id and not isinstance(self.type_id, int):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Type ID must be an integer.",
            )
        return self


class EntertainmentCreateSchema(EntertainmentUpdate):
    media_path: str | None = None
    media_type: str | None = Field(
        default=None,
        description="Media type. Can be either 'docs', 'music', 'video'",
    )

    @model_validator(mode="after")
    def validate_fields(self) -> "EntertainmentCreateSchema":
        if not self.title:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Title cannot be empty."
            )
        supported_media_types = {"docs", "music", "video"}
        if self.media_type not in supported_media_types:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid media type. Valid media types are: {', '.join(supported_media_types)}.",
            )
        if not self.type_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Type ID cannot be empty.",
            )
        if not self.media_path:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Media path cannot be empty.",
            )
        return self


class EntertainmentResponseSchema(EntertainmentBase):
    id: int
    message_id: int | None = None
    created_at: datetime
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class EntertainmentListResponseSchema(PaginationSchema):
    filter: int | None = None
    items: list[EntertainmentResponseSchema] = Field(
        default_factory=list, description="List of entertainments."
    )

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="after")
    def validate_items(self) -> "EntertainmentListResponseSchema":
        if not self.items:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No entertainments found."
            )
        return self


class EntertainmentQuerySchema(QueryParamsSchema):
    filter: int | None = Field(default=None, description="Filter by type ID.", gt=0)

    @model_validator(mode="after")
    def validate_filter_sort_search(self) -> "EntertainmentQuerySchema":
        if self.filter:
            if not isinstance(self.filter, int):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Filter must be an integer.",
                )
            if self.filter <= 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Filter must be greater than 0.",
                )

        return self


class EntertainmentTypesSchema(BaseModel):
    name: str | None = None

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="after")
    def validate_name(self) -> "EntertainmentTypesSchema":
        if not self.name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Name cannot be empty."
            )
        return self


class EntertainmentTypesResponseSchema(EntertainmentTypesSchema):
    id: int
    created_at: datetime
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
