from pydantic import BaseModel, ConfigDict
from datetime import datetime

from app.api.schemas.pagination import PaginationSchema


class ChannelBase(BaseModel):
    name: str
    link: str
    channel_id: int
    is_active: bool = True
    till: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class CreateChannel(ChannelBase):
    till: datetime | None = None


class UpdateChannel(BaseModel):
    name: str | None = None
    link: str | None = None
    channel_id: int | None = None
    is_active: bool | None = None
    till: datetime | None = None

    model_config = ConfigDict(from_attributes=True, extra='forbid')


class ChannelResponseSchema(ChannelBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ChannelListResponseSchema(PaginationSchema):
    items: list[ChannelResponseSchema]

    model_config = ConfigDict(from_attributes=True)
