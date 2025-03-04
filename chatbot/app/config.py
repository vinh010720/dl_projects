from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    together_api_key: str = Field(..., env="TOGETHER_API_KEY")
    redis_url: str = Field("redis://localhost:6379/0", env="REDIS_URL")
    whisper_model: str = "whisper-1"
    llama_model: str = "meta-llama/Llama-3.3-70B-Instruct-Turbo"
    gpt_eval_model: str = "gpt-4o-mini"
    api_timeout: int = 30

    class Config:
        env_file = ".env"
        extra = "ignore"  # Cho phép bỏ qua các input không được khai báo

settings = Settings()