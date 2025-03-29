import functools
import pathlib
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Project settings."""

    model_config = SettingsConfigDict(env_file=".env")

    BASE_DIR: pathlib.Path = pathlib.Path(__file__).resolve().parent.parent
    ENVIRONMENT: str = "local"

    CORS_ALLOW_ORIGIN_LIST: str = "http://localhost:8000"
    SESSION_MIDDLEWARE_SECRET: str = "secret"

    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    YA_CLIENT_ID: str
    YA_SECRET: str

    ADMIN_ID: Optional[int] = None  # Get from user info

    MAX_FILE_SIZE_IN_MB: int = 5

    @property
    def cors_allow_origins(self) -> list[str]:
        return self.CORS_ALLOW_ORIGIN_LIST.split("&")

    @property
    def postgres_dsn(self) -> str:
        database = (
            self.POSTGRES_DB
            if self.ENVIRONMENT != "test"
            else f"{self.POSTGRES_DB}_test"
        )
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{database}"
        )


@functools.lru_cache
def settings() -> Settings:
    return Settings()
