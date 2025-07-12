from __future__ import annotations
from pydantic import BaseModel, Field, ConfigDict, model_validator
from .pagination import PaginationSchema
from fastapi import HTTPException, status


class UserBase(BaseModel):
    phone_number: int | None = Field(
        default=123456789, description="International phone number"
    )

    @model_validator(mode="after")
    def validate_phone_number(self) -> "UserBase":
        if not self.phone_number:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Phone number is required.",
            )
        return self

    model_config = ConfigDict(from_attributes=True)


class UserResponseSchema(UserBase):
    id: int
    first_name: str
    last_name: str | None = None
    telegram_id: int
    language: str
    profile_picture: str | None = None
    is_admin: bool


class UserListResponseSchema(PaginationSchema):
    items: list[UserResponseSchema]

    @model_validator(mode="after")
    def validate_filter_sort_search(self) -> "UserListResponseSchema":
        if self.filter:
            valid_filters = ["is_admin", "language"]
            if self.filter.lstrip("-") not in valid_filters:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid filter field. Valid filters are: {', '.join(valid_filters)}",
                )

        if self.sort:
            valid_sorts = [
                "id",
                "first_name",
                "last_name",
                "telegram_id",
                "phone_number",
                "language",
                "is_admin",
                "created_at",
                "updated_at",
            ]
            if self.sort.lstrip("-") not in valid_sorts:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid sort field. Valid sorts are: {', '.join(valid_sorts)}",
                )
        if self.search:
            valid_search_fields = [
                "first_name",
                "last_name",
                "telegram_id",
                "phone_number",
            ]
            if self.search_field and self.search_field not in valid_search_fields:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid search field. Valid search fields are: {', '.join(valid_search_fields)}",
                )
        return self


class UserUpdateSchema(UserBase):
    first_name: str | None = Field(default="John", description="User's first name")
    last_name: str | None = Field(default="Doe", description="User's last name")
    is_admin: bool | None = Field(default=False, description="User's admin status")

    model_config = ConfigDict(from_attributes=True, extra="forbid")

    @model_validator(mode="after")
    def validate_update_fields(self) -> "UserUpdateSchema":
        if (
            not self.first_name
            and not self.last_name
            and self.phone_number is None
            and self.is_admin is None
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least one field must be provided for update.",
            )
        return self
