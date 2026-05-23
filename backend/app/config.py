"""Centralized environment settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    vision_provider: str = ''
    vision_api_key: str = ''
    vision_api_base_url: str = ''
    vision_model: str = ''
    openai_api_key: str = ''
    chat_api_key: str = ''
    chat_api_base_url: str = ''
    chat_model: str = ''
    database_url: str = ''
    cors_allow_origins: str = ''
    github_discussion_url: str = ''

    @property
    def cors_allow_origins_list(self) -> list[str]:
        """Expand comma-separated origins while ignoring empty items."""
        return [origin.strip() for origin in self.cors_allow_origins.split(',') if origin.strip()]


settings = Settings()
