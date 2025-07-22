from functools import cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    # API
    BASE_URL: str

    DEBUG: bool = False

    # BOT CONFIGURATION
    BOT_TOKEN: str
    TG_CHANNEL_ID: int
    TELEGRAM_STATE_DB: int

    # POSTGRES CREDENTIALS
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DB: str

    # REDIS CREDENTIALS
    REDIS_HOST: str
    REDIS_PORT: str
    REDIS_PASSWORD: str
    REDIS_DB: int = 0

    # JWT CONFIGURATION
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    # OPENAI CREDENTIALS
    OPENAI_API_KEY: str

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

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

    @property
    def ADMINS_TG_IDS(self) -> set[int]:
        return {
            6521856185,
        }


@cache
def get_settings() -> Settings:
    return Settings()  # noqa
