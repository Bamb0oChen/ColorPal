"""集中读取环境变量；所有敏感配置只在此处出现。"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    openai_api_key: str = ''
    database_url: str = 'sqlite+aiosqlite:///./data/colorpal.db'
    cors_allow_origins: str = 'http://localhost:5173'

    @property
    def cors_allow_origins_list(self) -> list[str]:
        """逗号分隔的多域名展开成 list，去掉空项。"""
        return [origin.strip() for origin in self.cors_allow_origins.split(',') if origin.strip()]


settings = Settings()
