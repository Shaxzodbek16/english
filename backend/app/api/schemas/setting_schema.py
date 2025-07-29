from datetime import datetime

from pydantic import BaseModel, model_validator, ConfigDict
from fastapi import HTTPException, status


class SettingSchema(BaseModel):
    settings: dict | None = None

    model_config = ConfigDict(from_attributes=True)


class SettingCreateSchema(SettingSchema):
    @model_validator(mode="after")
    def validate_settings(self):
        if self.settings is None or not isinstance(self.settings, dict):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Settings must be a dictionary.",
            )
        return self


class SettingUpdateSchema(SettingCreateSchema):
    pass


class SettingResponseSchema(SettingSchema):
    id: int
