"""Centralized environment settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    openai_api_key: str = ''
    database_url: str = 'sqlite+aiosqlite:///./data/colorpal.db'
    cors_allow_origins: str = 'http://localhost:5173,http://127.0.0.1:5173'
    github_discussion_url: str = 'https://github.com/Bamb0oChen/ColorPal/discussions'

    @property
    def cors_allow_origins_list(self) -> list[str]:
        """Expand comma-separated origins while ignoring empty items."""
        return [origin.strip() for origin in self.cors_allow_origins.split(',') if origin.strip()]


settings = Settings()
