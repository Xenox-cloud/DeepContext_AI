"""
Application Configuration Module

Provides centralized configuration management using environment variables
and Pydantic Settings for type-safe configuration.
"""

from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Settings(BaseSettings):
    """Application settings."""

    # Application
    app_name: str = "enterprise_nlp_platform"
    app_version: str = "1.0.0"
    debug: bool = False
    environment: str = "production"

    # Database
    database_url: str = (
        "sqlite+aiosqlite:///./enterprise_nlp.db"
    )

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # Qdrant
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    qdrant_collection_name: str = "documents"

    # Celery
    celery_broker_url: str = (
        "redis://localhost:6379/1"
    )

    celery_result_backend: str = (
        "redis://localhost:6379/2"
    )

    # API
    api_v1_prefix: str = "/api/v1"
    groq_api_key: str = ""
    secret_key: str = (
        "your-secret-key-here-change-in-production"
    )

    algorithm: str = "HS256"

    access_token_expire_minutes: int = 30

    # Upload
    upload_dir: str = "./uploads"

    max_upload_size: int = 10485760

    # Logging
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    @field_validator(
        "database_url",
        mode="before",
    )
    @classmethod
    def validate_database_url(
        cls,
        v: str
    ) -> str:

        allowed_prefixes = (
            "postgresql+",
            "sqlite+",
        )

        if not v.startswith(
            allowed_prefixes
        ):

            raise ValueError(
                "DATABASE_URL must start with "
                "'postgresql+' or 'sqlite+'"
            )

        return v


@lru_cache
def get_settings():

    return Settings()


settings = get_settings()