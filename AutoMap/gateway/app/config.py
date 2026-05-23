from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    backend_base_url: str = "http://localhost:5000"
    openai_api_key: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
