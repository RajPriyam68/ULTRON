from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="ULTRON_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    app_name: str = "ULTRON"
    app_version: str = "0.1.0"
    sprint: int = 0
    log_level: str = "INFO"
    debug: bool = False
    data_dir: Path | None = None
    window_width: int = Field(default=1440, ge=1024, le=3840)
    window_height: int = Field(default=900, ge=700, le=2160)
    ollama_base_url: str = "http://127.0.0.1:11434"
    ollama_model: str = "llama3.2"

    @field_validator("log_level")
    @classmethod
    def normalize_log_level(cls, value: str) -> str:
        level = value.strip().upper()
        allowed = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if level not in allowed:
            raise ValueError(f"log_level must be one of {sorted(allowed)}")
        return level


class UserLlmSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    user_llm_api_key: str = ""
    user_llm_base_url: str = ""
    user_llm_model: str = ""

    def is_configured(self) -> bool:
        return bool(self.user_llm_api_key and self.user_llm_base_url)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


@lru_cache(maxsize=1)
def get_user_llm_settings() -> UserLlmSettings:
    return UserLlmSettings()


def reset_settings() -> None:
    get_settings.cache_clear()
    get_user_llm_settings.cache_clear()
