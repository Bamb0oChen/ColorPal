"""集中读取环境变量；所有敏感配置只在此处出现。"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    vision_provider: str = 'qwen'
    vision_api_key: str = ''
    vision_api_base_url: str = (
        'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions'
    )
    vision_model: str = 'qwen-vl-max'
    database_url: str = 'sqlite:///./data/colorpal.db'
    cors_allow_origins: str = 'http://localhost:5173'

    @property
    def cors_allow_origins_list(self) -> list[str]:
        """逗号分隔的多域名展开成 list，去掉空项。"""
        return [origin.strip() for origin in self.cors_allow_origins.split(',') if origin.strip()]


settings = Settings()
