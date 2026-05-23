"""FastAPI 配置管理"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # 服务配置
    GATEWAY_HOST: str = "0.0.0.0"
    GATEWAY_PORT: int = 8000
    CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]

    # OpenAI
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4-vision-preview"

    # 数据库
    DATABASE_URL: str = "sqlite:///./colopal.db"

    class Config:
        env_file = "../.env"
        env_file_encoding = "utf-8"


settings = Settings()
