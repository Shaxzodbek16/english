from pydantic import BaseModel, ConfigDict, model_validator
from fastapi import HTTPException, status


class MediaClearSchema(BaseModel):
    media_path: str | None = None

    @model_validator(mode="after")
    def validate_media_path(self):
        if not self.media_path:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Media path is required.",
            )
        if not isinstance(self.media_path, str):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Media path must be a string.",
            )
        return self

    model_config = ConfigDict(from_attributes=True)


class MediaSchemaResponse(MediaClearSchema):
    media_url: str

    model_config = ConfigDict(from_attributes=True)
