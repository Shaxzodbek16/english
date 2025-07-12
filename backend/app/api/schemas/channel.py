from pydantic import BaseModel, ConfigDict, model_validator
from datetime import datetime
from fastapi import HTTPException, status

from app.api.schemas.pagination import PaginationSchema


class ChannelBase(BaseModel):
    name: str | None = None
    link: str | None = None
    channel_id: int | None = None
    is_active: bool | None = None
    till: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class CreateChannelSchema(ChannelBase):
    @model_validator(mode="after")
    def validate_data(self) -> "ChannelBase":
        if not self.name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Name cannot be empty.",
            )
        if not self.link:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Link cannot be empty.",
            )
        if not isinstance(self.channel_id, int):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Channel ID must be a positive integer.",
            )
        if self.is_active not in [True, False]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="is_active must be a boolean value.",
            )
        return self

    model_config = ConfigDict(from_attributes=True)


class UpdateChannelSchema(ChannelBase):
    @model_validator(mode="after")
    def validate_update_data(self) -> "UpdateChannelSchema":
        if not any([self.name, self.link, self.channel_id, self.is_active, self.till]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least one field must be provided for update.",
            )
        return self

    model_config = ConfigDict(from_attributes=True, extra="forbid")


class ChannelResponseSchema(ChannelBase):
    id: int
    created_at: datetime
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class ChannelListResponseSchema(PaginationSchema):
    items: list[ChannelResponseSchema]
    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="after")
    def validate_filter_or_sort(self) -> "ChannelListResponseSchema":
        if self.filter:
            valid_filters = ["is_active"]
            if not self.filter.lstrip("-") in valid_filters:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid filter field. Valid filters are: {', '.join(valid_filters)}",
                )
        if self.sort:
            valid_sorts = [
                "id",
                "name",
                "link",
                "channel_id",
                "is_active",
                "till",
                "created_at",
                "updated_at",
            ]
            if not self.sort.lstrip("-") in valid_sorts:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid sort field. Valid sorts are: {', '.join(valid_sorts)}",
                )
        return self
