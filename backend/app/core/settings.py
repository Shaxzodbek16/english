from functools import cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    # API
    BASE_URL: str

    # POSTGRES CREDENTIALS
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DB: str

    # JWT CONFIGURATION
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    model_config = SettingsConfigDict(env_file=".env")

    @property
    def get_postgres_url(self):
        return f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def base_dir(self) -> Path:
        return Path(__file__).parent.parent.parent

    @property
    def get_base_media_dir(self) -> Path:
        return self.base_dir / "media"

    @property
    def get_base_static_dir(self) -> Path:
        return self.base_dir / "static"

    @property
    def API_V1_STR(self, version: str = "v1") -> str:
        return f"/api/{version}"


@cache
def get_settings() -> Settings:
    return Settings()  # noqa
