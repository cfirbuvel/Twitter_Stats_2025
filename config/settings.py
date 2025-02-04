from pydantic_settings import BaseSettings
from pydantic import Field, SecretStr, ValidationError
import sys

class Settings(BaseSettings):
    TG_API_ID: int = Field(..., env="TG_API_ID")
    TG_API_HASH: SecretStr = Field(..., env="TG_API_HASH")
    TG_BOT_TOKEN: SecretStr = Field(..., env="TG_BOT_TOKEN")
    TWITTER_BEARER_TOKEN: SecretStr = Field(..., env="TWITTER_BEARER_TOKEN")
    BOT_PASSWORD: SecretStr = Field(..., env="BOT_PASSWORD")
    REDIS_URL: str = Field("redis://redis:6379/0", env="REDIS_URL")

    class Config:
        env_file = ".env"

try:
    settings = Settings()
except ValidationError as e:
    print("❌ Missing or invalid environment variables:", e)
    sys.exit(1)