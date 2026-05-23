"""Centralized environment settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    vision_provider: str = 'qwen'
    vision_api_key: str = ''
    vision_api_base_url: str = (
        'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions'
    )
    vision_model: str = 'qwen-vl-max'
    openai_api_key: str = ''
    chat_api_key: str = ''
    chat_api_base_url: str = ''
    chat_model: str = ''
    database_url: str = 'sqlite:///./data/colorpal.db'
    cors_allow_origins: str = 'http://localhost:5173,http://127.0.0.1:5173'
    github_discussion_url: str = 'https://github.com/Bamb0oChen/ColorPal/discussions'

    @property
    def cors_allow_origins_list(self) -> list[str]:
        """Expand comma-separated origins while ignoring empty items."""
        return [origin.strip() for origin in self.cors_allow_origins.split(',') if origin.strip()]


settings = Settings()
