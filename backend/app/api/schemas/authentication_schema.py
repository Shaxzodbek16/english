from pydantic import BaseModel, ConfigDict


class RefreshTokenSchema(BaseModel):
    refresh_token: str

    model_config = ConfigDict(from_attributes=True)


class TokenResponseSchema(RefreshTokenSchema):
    access_token: str
    token_type: str = "Bearer"

    model_config = ConfigDict(from_attributes=True)
