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
    public_api_base_url: str = 'http://localhost:8000'
    github_discussion_url: str = ''

    @property
    def cors_allow_origins_list(self) -> list[str]:
        if self.cors_allow_origins:
            return [origin.strip() for origin in self.cors_allow_origins.split(',') if origin.strip()]
        return [f'http://localhost:{p}' for p in range(5173, 5190)] + [f'http://127.0.0.1:{p}' for p in range(5173, 5190)]


settings = Settings()
